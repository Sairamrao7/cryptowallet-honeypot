from flask import Blueprint, request, jsonify, send_file
from .models import db, WalletImport, SendAttempt, BehaviorLog
from sqlalchemy.exc import SQLAlchemyError
import hashlib
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

main_bp = Blueprint('main', __name__)

# Helper functions
def hash_credential(credential):
    return hashlib.sha256(credential.encode()).hexdigest()

def truncate_ip(ip):
    if ':' in ip:  # IPv6
        return ip.split(':')[0] + '::'
    parts = ip.split('.')
    return '.'.join(parts[:2]) + '.x.x' if len(parts) == 4 else ip

def virus_total_check(data):
    # Dummy fallback
    return {'malicious': False, 'source': 'dummy'}

def hibp_check(credential_hash):
    # Dummy fallback
    return {'pwned': False, 'source': 'dummy'}

# API Endpoints
@main_bp.route('/import-wallet', methods=['POST'])
def import_wallet():
    data = request.json
    wallet_type = data.get('wallet_type')
    credential = data.get('credential')
    ip = truncate_ip(request.remote_addr or '0.0.0.0')
    user_agent = request.headers.get('User-Agent', '')
    credential_hash = hash_credential(credential)
    vt_result = virus_total_check(credential)
    hibp_result = hibp_check(credential_hash)
    wi = WalletImport(ip=ip, user_agent=user_agent, wallet_type=wallet_type, credential_hash=credential_hash)
    db.session.add(wi)
    db.session.commit()
    return jsonify({'success': True, 'vt': vt_result, 'hibp': hibp_result})

@main_bp.route('/get-balance', methods=['GET'])
def get_balance():
    # Fake balance
    return jsonify({'balance': 12.345, 'currency': 'ETH'})

@main_bp.route('/send', methods=['POST'])
def send():
    data = request.json
    to_address = data.get('to_address')
    amount = data.get('amount')
    credential = data.get('credential')
    ip = truncate_ip(request.remote_addr or '0.0.0.0')
    user_agent = request.headers.get('User-Agent', '')
    credential_hash = hash_credential(credential)
    vt_result = virus_total_check(to_address)
    sa = SendAttempt(ip=ip, user_agent=user_agent, to_address=to_address, amount=amount, credential_hash=credential_hash)
    db.session.add(sa)
    db.session.commit()
    return jsonify({'success': True, 'vt': vt_result, 'txid': '0xFAKE123'})

@main_bp.route('/behavior-log', methods=['POST'])
def behavior_log():
    data = request.json
    typing_speed = data.get('typing_speed')
    mouse_movements = data.get('mouse_movements')
    session_id = data.get('session_id')
    ip = truncate_ip(request.remote_addr or '0.0.0.0')
    user_agent = request.headers.get('User-Agent', '')
    bl = BehaviorLog(ip=ip, user_agent=user_agent, typing_speed=typing_speed, mouse_movements=str(mouse_movements), session_id=session_id)
    db.session.add(bl)
    db.session.commit()
    return jsonify({'success': True})

@main_bp.route('/report', methods=['GET'])
def report():
    format = request.args.get('format', 'pdf')
    wi = WalletImport.query.all()
    sa = SendAttempt.query.all()
    bl = BehaviorLog.query.all()
    # DataFrames
    wi_df = pd.DataFrame([w.__dict__ for w in wi]).drop('_sa_instance_state', axis=1, errors='ignore')
    sa_df = pd.DataFrame([s.__dict__ for s in sa]).drop('_sa_instance_state', axis=1, errors='ignore')
    bl_df = pd.DataFrame([b.__dict__ for b in bl]).drop('_sa_instance_state', axis=1, errors='ignore')
    # Graph
    plt.figure(figsize=(6,4))
    if not wi_df.empty:
        wi_df['timestamp'] = pd.to_datetime(wi_df['timestamp'])
        wi_df.groupby(wi_df['timestamp'].dt.date).size().plot(kind='bar')
        plt.title('Wallet Imports per Day')
        plt.tight_layout()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    if format == 'csv':
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            wi_df.to_excel(writer, sheet_name='WalletImports')
            sa_df.to_excel(writer, sheet_name='SendAttempts')
            bl_df.to_excel(writer, sheet_name='BehaviorLogs')
        output.seek(0)
        return send_file(output, download_name='report.xlsx', as_attachment=True)
    else:
        pdf = BytesIO()
        c = canvas.Canvas(pdf)
        c.drawString(100, 800, 'Honeypot Threat Report')
        image_for_pdf = ImageReader(img)
        c.drawImage(image_for_pdf, 100, 600, width=400, height=150)
        c.drawString(100, 580, f'Total Wallet Imports: {len(wi_df)}')
        c.drawString(100, 560, f'Total Send Attempts: {len(sa_df)}')
        c.drawString(100, 540, f'Total Behavior Logs: {len(bl_df)}')
        c.showPage()
        c.save()
        pdf.seek(0)
        return send_file(pdf, download_name='report.pdf', as_attachment=True)