import requests

class IrrigationController:
    def send_command(self, zone_id, amount_mm):
        """
        Simula o envio de um comando para um sistema de irrigação.
        Em uma implementação real, esta função faria uma requisição para a API do dispositivo.
        """
        api_url = "http://api.seu-sistema-irrigation.com/command" # URL fictícia
        payload = {
            "zone_id": zone_id,
            "amount_mm": amount_mm
        }
        
        try:
            # response = requests.post(api_url, json=payload)
            # response.raise_for_status() # Lança um erro para status HTTP ruins
            print(f"Comando de irrigação enviado com sucesso para a zona {zone_id}: {amount_mm}mm")
            return {"status": "success", "message": "Comando enviado"}
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar comando de irrigação: {e}")
            return {"status": "error", "message": str(e)}
