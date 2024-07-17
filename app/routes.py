
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session, current_app
from pyad import aduser, pyad, adquery
from ldap3 import Server, Connection, ALL
from netmiko import ConnectHandler
from .models import Database, Device, MdtaRegion, Config


main = Blueprint('main', __name__)

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        
        """
        # Hostname                         IPv4Address
        # --------                         -----------
        # MDTAICCDC03.mdta.ad.mdot.mdstate 10.93.121.41
        # MDTAICCDC01.mdta.ad.mdot.mdstate 10.93.121.40
        # MDTAJFKDC01.mdta.ad.mdot.mdstate 10.93.119.40
        # MDTAJFKDC02.mdta.ad.mdot.mdstate 10.93.119.41
        # mdtaazdc01.mdta.ad.mdot.mdstate  10.91.252.9
        """
        current_app.config['AD_SERVER'] = '10.93.121.40'
        ad_server = current_app.config['AD_SERVER']
        current_app.config['AD_DOMAIN'] = 'mdta'
        ad_domain = current_app.config['AD_DOMAIN']
        ad_domain = f"{ad_domain}"
        user_dn = f'{ad_domain}\\{username}'

        server = Server(ad_server, get_info=ALL)
        try:
            conn = Connection(server, user=user_dn, password=password)
            if conn.bind():
                conn.unbind()
                return True
        except Exception as e:
            print(f"Authentication failed: {e}")
        return False


@main.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if AuthService.authenticate_user(username, password):
            session['username'] = username
            session['password'] = password
            return redirect(url_for('main.dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('main.login'))

@main.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('main.login'))

@main.route('/add_device', methods=['POST'])
def add_device():
    if 'username' in session:
        name = request.form['name']
        ip_address = request.form['ip_address']

        device = Device(name=name, ip_address=ip_address)
        Database.db.session.add(device)
        Database.db.session.commit()

        return jsonify({'message': 'Device added successfully'}), 201
    return jsonify({'error': 'Unauthorized'}), 401

@main.route('/run_command', methods=['POST'])
def run_command():
    if 'username' in session:
        device_id = request.form['device_id']
        command = request.form['command']

        device = Device.query.get(device_id)

        if device:
            netmiko_device = {
                'device_type': 'cisco_ios',
                'host': device.ip_address,
                'username': session['username'],
                'password': session['password'],
            }

            try:
                connection = ConnectHandler(**netmiko_device)
                output = connection.send_command(command)
                connection.disconnect()
                return jsonify({'output': output}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Device not found'}), 404
    return jsonify({'error': 'Unauthorized'}), 401

@main.route('/set_config', methods=['POST'])
def set_config():
    if 'username' in session:
        key = request.form['key']
        value = request.form['value']

        config = Config.query.filter_by(key=key).first()
        if config:
            config.value = value
        else:
            config = Config(key=key, value=value)
            Database.db.session.add(config)
        Database.db.session.commit()

        return jsonify({'message': 'Configuration set successfully'}), 201
    return jsonify({'error': 'Unauthorized'}), 401

@main.route('/network_interfaces/<int:asset_id>', methods=['GET'])
def network_interfaces(asset_id):
    lansweeper_db = get_lansweeper_db()
    try:
        interfaces = lansweeper_db.get_network_interfaces(asset_id)
        return jsonify(interfaces), 200
    except pyodbc.Error as err:
        return jsonify({'error': str(err)}), 500

@main.route('/assets', methods=['GET'])
def assets():
    lansweeper_db = get_lansweeper_db()
    try:
        assets = lansweeper_db.get_all_assets()
        return jsonify(assets), 200
    except pyodbc.Error as err:
        return jsonify({'error': str(err)}), 500
    
    
    
@main.route('/test')
def test():
    return render_template('sampleAjax1.html')
