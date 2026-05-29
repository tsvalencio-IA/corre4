Olympikus Corre 4 — Sistema 3D e AR (Demo)
==========================================

Este pacote demonstra um sistema de visualização 3D e realidade aumentada para o tênis **Olympikus Corre 4**. Foi construído para ser publicado no GitHub Pages ou em qualquer servidor web estático. Ao abrir `index.html` no navegador do celular (preferencialmente Android com Chrome), o visitante poderá:

* Girar e ampliar o modelo 3D do tênis.
* Tocar no botão “Ver em Realidade Aumentada” para ativar o AR via WebXR/Scene Viewer.
* Consultar fotos de referência do produto reais, incluídas na pasta `photos/`.

Como funciona o modelo 3D
------------------------

O arquivo `models/corre-4-estilo-vermelho.glb` incluído neste pacote **não é genérico**. Ele foi construído manualmente a partir das fotos do tênis, reproduzindo a forma da entressola, cabedal, cadarços, língua e os detalhes de textura e da lateral “CORRE”.  Este GLB é, portanto, um modelo estilizado/desenhado que procura se aproximar do aspecto visual do **Olympikus Corre 4** sem recorrer a fotogrametria pesada.  Ao abrir a página, você verá esse modelo girando automaticamente e pode interagir com ele em 360° ou colocá‑lo em Realidade Aumentada.

Para obter um resultado **ainda mais fiel**, você pode escanear o tênis real utilizando um aplicativo de fotogrametria como **Polycam** ou **KIRI Engine**. Esses apps capturam dezenas de fotos e geram modelos 3D em formatos como GLB/GLTF. Caso deseje substituir o modelo desenhado por um escaneado:

1. Faça o escaneamento do tênis e exporte o modelo final em formato `.glb`.
2. Renomeie o arquivo exportado para `corre-4-estilo-vermelho.glb`.
3. Substitua o arquivo existente em `models/` pelo novo modelo.
4. Reenvie a pasta completa para o GitHub Pages. O sistema passará a carregar o modelo escaneado na página e na Realidade Aumentada.

Estrutura de pastas
-------------------

```
corre4-sistema-completo/
  ├── index.html               # página principal com modelo 3D e AR
  ├── models/
  │   └── corre-4-estilo-vermelho.glb  # modelo 3D genérico (substitua pelo oficial)
  ├── photos/
  │   ├── top.jpg              # vista superior do tênis
  │   ├── sole.jpg             # sola
  │   ├── side1.jpg            # lateral interna
  │   ├── side2.jpg            # lateral externa
  │   └── back.jpg             # traseira
  └── README.txt               # este arquivo de instruções
```

Limitações e considerações
--------------------------

* O modelo GLB fornecido é um **modelo estilizado** construído manualmente a partir das fotos. Ele captura diversos elementos do design, mas não é uma fotogrametria milimétrica do produto. Para obter fidelidade visual absoluta, é indispensável substituir por um modelo escaneado.
* A função de detecção de pé e encaixe automático em AR, implementada anteriormente com MediaPipe Pose, não está incluída nesta versão minimalista. Ela pode ser adicionada em scripts JavaScript caso você deseje avançar com o alinhamento automático do tênis no pé do usuário.
* Ao publicar no GitHub Pages, lembre-se de ativar o HTTPS e utilizar um navegador compatível com WebXR para que o botão de Realidade Aumentada funcione corretamente.
