from flask import Flask, render_template, request, jsonify
import threading
import requests
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_reports', methods=['POST'])
def send_reports():
    data = request.get_json()
    profile_link = data['profileLink']
    num_reports = int(data['numReports'])

    def run_bot():
        url = "https://mssdk-va.tiktok.com/web/report"
        params = {
            'msToken': 'PuRm1TUYjZprBbxH6dbZe_kS8AgBrWxeLniFaobcXp8jLREivrzvhcg5nksBUD-9ksTtjazJ-PeaTKw5G0Ku5ZvHGB6yFiqEwBIUGfN3u15bM46UXp1arS6WfCIAuziaAjKIMAhZ-lFzijVhlbkY',
            'X-Bogus': 'DFSzswVuRxCuFHRmtwIo-MSscjcL'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': '_ttp=29VNfaKGWtgyiop3agwuPOGUoTC; tt_csrf_token=x7jdy1sm-cEAORZHLdFVrDcVmH4Cntr9_bn0; ak_bmsc=8559B691C8DC86A764BD2A501F3E526F~000000000000000000000000000000~YAAQHUZbaBWcNpGQAQAA0kHgpxgT6utwQbma3yrspKDS9XD94C8c3M7BMqZ8PA/EeKOOu2rZ9BBpSJo1eWg689qvDlS6WxrKvdNMxc9bTE77dCG/dbHkCIa7kjdIfKiMoYGDg6bmeDenaiLRbL0cBAE8yU3m1fYzK61rWYwhZont4pqiXPehVmWb+3xGuooOm1S770PZJZyD7ALaVt3ROG7ruwxpQZP/l6BxNwIFDjIrebc7hbx5I4536F7HqzK8jtpwhqBuu6TYx2uKHtwAyYns3d9233GHlgn4AvbaEAfCfXq9a4r5/VGpgqhGnkOSy9LZwKw0eLytL4MP1rGaiqAPIIidBmeY0dUeXSCPFmGblQRAuI3KZmlkIrytjUZ8yYT4dNMi7ZMJ; passport_csrf_token=91d39ed6cccfca04495a5a5e9825b1ee; passport_csrf_token_default=91d39ed6cccfca04495a5a5e9825b1ee; s_v_web_id=verify_lyixxlhx_BQruPEyc_LPto_4cr1_9S7o_ofnp6yHliiFK; d_ticket=d6494d3616f9b6f01513445d94b0e8704e3fe; multi_sids=7028579659419878406%3A87d8311889d72ae9e834d92f4b90886d; cmpl_token=AgQQAPMFF-RO0rG0aVGbcN0__PD5eUJX_4eOYNYHjw; sid_guard=87d8311889d72ae9e834d92f4b90886d%7C1720803583%7C15551999%7CWed%2C+08-Jan-2025+16%3A59%3A42+GMT; uid_tt=386aa77cb262d2fb3edf92cd4c7bc4759f282ded8651c7df99cf781173bbd932; uid_tt_ss=386aa77cb262d2fb3edf92cd4c7bc4759f282ded8651c7df99cf781173bbd932; sid_tt=87d8311889d72ae9e834d92f4b90886d; sessionid=87d8311889d72ae9e834d92f4b90886d; sessionid_ss=87d8311889d72ae9e834d92f4b90886d; sid_ucp_v1=1.0.0-KGQ5M2U3NzE2NDg1OGI2ZTlmODAyODM0N2YxNzBmZGFlMzAyN2NmMDEKIgiGiIia4f6hxWEQ_8HFtAYYswsgDDCxkKqMBjgBQOoHSAQQAxoGbWFsaXZhIiA4N2Q4MzExODg5ZDcyYWU5ZTgzNGQ5MmY0YjkwODg2ZA; ssid_ucp_v1=1.0.0-KGQ5M2U3NzE2NDg1OGI2ZTlmODAyODM0N2YxNzBmZGFlMzAyN2NmMDEKIgiGiIia4f6hxWEQ_8HFtAYYswsgDDCxkKqMBjgBQOoHSAQQAxoGbWFsaXZhIiA4N2Q4MzExODg5ZDcyYWU5ZTgzNGQ5MmY0YjkwODg2ZA; store-idc=maliva; store-country-code=ng; store-country-code-src=uid; tt-target-idc=useast1a; tt-target-idc-sign=PuFpVdnZlEMUHQIjeCiINWdDbCvjYVeiHcbm-L8zvRV-r3jDboQUddbCDaVGV1yGPFRQs7tMVpkNHyO1PoQeSvNevEXLBQFV6mNvSIpv7sH9Q3s2LYdCdd89Ch9HKlULjvJcfkH-jvdpedc7LssgW_wsHWcMwGS0F0Qa_rd4aT_q_gyufYCktIiIJoo6c28jJ67v7DLHGRQvnd--Nrh_iCprZUEDd6Er9gJCFbre_z8IdCmi9H1vILoO7jFzACI342d-ODzlhJy9335OHgFIPw2mt5q40WswX2lilSfXbALJs6ZlcYA7MS0wtbkJJymAQsAHcdGzaP4xz-oFcJKjKbiwyeYPjligsPKhL8TF_367zDKJZ2R0Df_AuHNrAxLaAbjz8aZFT3XgE-6V2wHlipIKpuyi1qqCWbGyT_p2WXj2FG_ZWCvlRnlzlBNhDPLHFZBPjslTBV2Pt_wUW1tq_scr1--kPSisNME-3X8vaIWVJbTjBrFj6LrDahZniDuO; tt_chain_token=aFGA0aSADJ5vKAWk9xeaDw==; bm_sv=47EED61F77304BF6A13A8A43442BD5C6~YAAQHEZbaACehX+QAQAA9PLipxh5iPKt98Bbo3aEGGWIhkO7XetFlBEQp5L2I1qmBVZHpCl4sOl8t6xyr0AmXpprX29KuylRwa5o9XV+KAIpRclyfbX0o7iJvKaOxbx0XFwfXKklEEEFu32VgPA8svRAR5YoEDPCPmRNWByL8U0lfEr+ddQ/7wlWqVzQm9pEBiHWw9ZShsZKJguzZd/jrzfsnTQUGeaxaqX2nUMy5aR8weCQz8cjb82/SiYnZiqI~1; ttwid=1%7CDDSj5KHrZxQ0KCTxTFkgkE8ATNrOimDFX--ABOYRTtw%7C1680535839%7Ce8e5a2292871c940d25859fe15b94724f6397dc97360ed9e75898e68b0c8ae52; csrf_session_id=a2bc20a7a086312e2fca3b2c6e08903b; csrf_session_id_ss=a2bc20a7a086312e2fca3b2c6e08903b; home_can_add_dy_ticket=1; home_can_add_dy_ticket_ss=1; ttwid_ss=1%7CDDSj5KHrZxQ0KCTxTFkgkE8ATNrOimDFX--ABOYRTtw%7C1680535839%7Ce8e5a2292871c940d25859fe15b94724f6397dc97360ed9e75898e68b0c8ae52',
            'Referer': 'https://www.tiktok.com/@maliwatts08?lang=en',
        }

        payload = {
            "scene": 40,
            "user_id": "7028579659419878406",
            "aweme_id": "7255542148709729582",
            "options": [
                {"type": 34, "value": 116},
                {"type": 49, "value": 245}
            ],
            "text": "The account is a scam account"
        }

        for i in range(num_reports):
            response = requests.post(url, headers=headers, json=payload, params=params)
            if response.status_code == 200:
                print(f"Report {i+1} submitted successfully")
            else:
                print(f"Failed to submit report {i+1}: {response.status_code}")
                print(response.text)
            time.sleep(1)  # Add a delay to avoid being blocked by TikTok

    thread = threading.Thread(target=run_bot)
    thread.start()

    return jsonify({'status': 'Reports sent successfully'})

if __name__ == '__main__':
    app.run(debug=True)
