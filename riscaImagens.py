from pathlib import Path
import cv2
import sys

if len(sys.argv) != 5:
    print('O programa recebe as coordenadas do bounding box a ser desenhado por args. Exemplo PUC: 0 185 1140 580')
    sys.exit(0)

raiz = Path(__file__).parent.resolve()
print('Raiz: ', raiz)
resp = input('O programa vai encontrar todas as imagens a partir da raiz e desenhar um bounding box. Para continuar, tecle s:')
if resp != 's':
    exit()

p1 = (int(sys.argv[1]),int(sys.argv[2]))
p2 = (int(sys.argv[3]),int(sys.argv[4]))

pathImgs = raiz.rglob('*.jpg')
for path in pathImgs:
    str = path.as_posix()
    img = cv2.imread(str)
    cv2.rectangle(img, p1, p2, (0,0,0), 2)
    cv2.imwrite(str, img)