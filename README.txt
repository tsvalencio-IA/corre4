CORRE 4 — GLB + SISTEMA GITHUB
===============================

Arquivos principais:
- index.html: visualização premium 360° do Corre 4.
- comparador.html: compara dois GLBs e permite upload local.
- provador-pe.html: abre câmera do celular e tenta encaixar o tênis automaticamente no pé.
- models/corre4.glb: arquivo GLB criado localmente, com peças e âncoras.
- tools/create_corre4_glb.py: script usado para gerar o GLB novamente, caso queira ajustar.

O QUE FOI CRIADO
----------------
Este pacote contém um GLB real, não apenas JSON vazio. O modelo tem geometria visível, materiais, peças nomeadas e âncoras de AR.

Peças principais no GLB:
- CABEDAL
- ENTRESSOLA
- SOLADO
- CADARCOS
- LINGUETA
- CONTRAFORTE
- PUXADOR_TRASEIRO
- LOGO_CORRE
- ETIQUETA_OLYMPIKUS
- DETALHES_SOLADO

Âncoras para encaixe no pé:
- FOOT_ANCHOR
- TOE_ANCHOR
- HEEL_ANCHOR
- SOLE_CENTER
- ANKLE_GUIDE
- INSTEP_GUIDE

COMO SUBIR NO GITHUB PAGES
--------------------------
1. Envie todo o conteúdo desta pasta para o repositório.
2. Mantenha a estrutura:
   index.html
   comparador.html
   provador-pe.html
   assets/
   models/corre4.glb
3. Ative o GitHub Pages.
4. Abra o link pelo Chrome do celular.

AR NO PÉ
--------
O arquivo provador-pe.html usa câmera + Three.js + MediaPipe Pose.
Ele tenta detectar calcanhar e ponta do pé e posicionar o GLB automaticamente.
Se o detector não carregar no navegador, o modo manual continua funcionando com controles de escala, altura, horizontal e rotação.

VERDADE TÉCNICA
---------------
Este GLB é um modelo procedural/estilizado gerado localmente. Ele é melhor que JSON vazio e já funciona em model-viewer/Three.js, mas ainda não é uma fotogrametria perfeita como um modelo feito por scanner profissional ou modelador 3D humano em Blender. A vantagem é que agora existe um GLB real no pacote, com malha, materiais e âncoras.

Powered by thIAguinho Soluções Digitais
