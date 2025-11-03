import qrcode
import cv2
import numpy as np

def gerar_qrcode(link, qr_path='qrcode.png'):
    """
    Gera QR Code a partir de um link
    """
    qr = qrcode.QRCode(
        version=4,  # Ajusta tamanho
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_path)
    print(f"QR Code gerado: {qr_path}")
    return qr_path

def converter_para_marker(qr_path='qrcode.png', patt_path='marker.patt'):
    """
    Converte QR Code para arquivo AR.js .patt
    """
    # Carrega imagem em escala de cinza
    img = cv2.imread(qr_path, cv2.IMREAD_GRAYSCALE)
    
    # Redimensiona para 64x64 px (AR.js padrão)
    img_small = cv2.resize(img, (64, 64), interpolation=cv2.INTER_AREA)
    
    # Normaliza pixels para 0 ou 1
    img_bin = (img_small > 128).astype(np.uint8)
    
    # Salva no formato .patt
    with open(patt_path, 'w') as f:
        f.write("!V3 marker\n")  # Cabeçalho AR.js
        for row in img_bin:
            f.write(" ".join(str(int(v)) for v in row) + "\n")
    
    print(f"Marcador AR gerado: {patt_path}")
    return patt_path

if __name__ == "__main__":
    link = input("Digite o link que o QR Code deve abrir: ")
    qr_file = gerar_qrcode(link, 'qrcode.png')
    patt_file = converter_para_marker(qr_file, 'marker.patt')
