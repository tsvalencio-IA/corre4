import numpy as np
import trimesh
from trimesh.transformations import translation_matrix, rotation_matrix
from trimesh.visual.material import PBRMaterial

# Materials
mat_upper = PBRMaterial(name='MAT_CABEDAL_VERMELHO', baseColorFactor=[0.78,0.02,0.05,1.0], metallicFactor=0.02, roughnessFactor=0.78)
mat_mid = PBRMaterial(name='MAT_ENTRESSOLA_VERMELHA', baseColorFactor=[0.86,0.05,0.10,1.0], metallicFactor=0.02, roughnessFactor=0.48)
mat_out = PBRMaterial(name='MAT_SOLADO_VERMELHO_ESCURO', baseColorFactor=[0.35,0.01,0.03,1.0], metallicFactor=0.0, roughnessFactor=0.90)
mat_lace = PBRMaterial(name='MAT_CADARCO_VERMELHO', baseColorFactor=[0.58,0.01,0.03,1.0], metallicFactor=0.0, roughnessFactor=0.95)
mat_logo = PBRMaterial(name='MAT_LOGO_BRANCO', baseColorFactor=[0.92,0.92,0.86,1.0], metallicFactor=0.05, roughnessFactor=0.42)
mat_dark = PBRMaterial(name='MAT_DETALHES_ESCUROS', baseColorFactor=[0.10,0.02,0.03,1.0], metallicFactor=0.0, roughnessFactor=0.80)
mat_mesh = PBRMaterial(name='MAT_MALHA_SOMBRA', baseColorFactor=[0.28,0.01,0.02,1.0], metallicFactor=0.0, roughnessFactor=0.95)
mat_anchor = PBRMaterial(name='MAT_ANCHOR_INVISIVEL', baseColorFactor=[0,0,0,0.0], metallicFactor=0.0, roughnessFactor=1.0)

scene = trimesh.Scene()

def add_mesh(mesh, name, material):
    mesh.visual.material = material
    scene.add_geometry(mesh, geom_name=name, node_name=name)
    return mesh

# helper profiles
def smoothstep(t):
    return t*t*(3-2*t)

def taper_profile(x, xmin=-0.155, xmax=0.165):
    # 0 at ends, 1 in middle with soft taper
    t = (x - xmin)/(xmax-xmin)
    left = smoothstep(np.clip(t/0.18,0,1))
    right = smoothstep(np.clip((1-t)/0.16,0,1))
    return np.minimum(left, right)

def create_tube(name, xmin, xmax, nx, nt, center_y_fn, width_fn, height_fn, material, cap=True):
    verts=[]; faces=[]
    for i,x in enumerate(np.linspace(xmin,xmax,nx)):
        cy=center_y_fn(x); w=width_fn(x); h=height_fn(x)
        for j,th in enumerate(np.linspace(0,2*np.pi,nt,endpoint=False)):
            z=w*np.sin(th)
            y=cy + h*np.cos(th)
            # subtle asymmetric side: lateral side a bit flatter/stronger
            if z > 0: y -= 0.005*(z/max(w,1e-6))**2
            verts.append([x,y,z])
    for i in range(nx-1):
        for j in range(nt):
            a=i*nt+j; b=i*nt+(j+1)%nt; c=(i+1)*nt+j; d=(i+1)*nt+(j+1)%nt
            faces.append([a,c,b]); faces.append([b,c,d])
    if cap:
        # cap start/end with centers
        start_center=len(verts); verts.append([xmin,center_y_fn(xmin),0])
        end_center=len(verts); verts.append([xmax,center_y_fn(xmax),0])
        for j in range(nt):
            faces.append([start_center,j,(j+1)%nt])
            a=(nx-1)*nt+j; b=(nx-1)*nt+(j+1)%nt
            faces.append([end_center,b,a])
    mesh=trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
    mesh.visual.material=material
    return mesh

xmin,xmax=-0.155,0.165

# Midsole / outsole
midsole = create_tube(
    'ENTRESSOLA', xmin, xmax, 64, 32,
    center_y_fn=lambda x: 0.020 + 0.010*np.exp(-((x-0.135)/0.038)**2) + 0.004*np.exp(-((x+0.135)/0.04)**2),
    width_fn=lambda x: (0.048 + 0.012*taper_profile(x))*(0.88 + 0.12*np.exp(-((x-0.03)/0.1)**2)),
    height_fn=lambda x: 0.025 + 0.007*taper_profile(x),
    material=mat_mid)
add_mesh(midsole,'ENTRESSOLA', mat_mid)

outsole = create_tube(
    'SOLADO', xmin+0.003, xmax-0.002, 64, 28,
    center_y_fn=lambda x: -0.012 + 0.006*np.exp(-((x-0.14)/0.04)**2),
    width_fn=lambda x: 0.046 + 0.014*taper_profile(x),
    height_fn=lambda x: 0.012 + 0.002*taper_profile(x),
    material=mat_out)
add_mesh(outsole,'SOLADO', mat_out)

# Upper (cabedal) rounded shell
upper = create_tube(
    'CABEDAL', xmin+0.008, xmax-0.01, 72, 34,
    center_y_fn=lambda x: 0.057 + 0.020*np.exp(-((x+0.095)/0.05)**2) + 0.006*np.exp(-((x-0.02)/0.09)**2) - 0.010*np.exp(-((x-0.145)/0.035)**2),
    width_fn=lambda x: (0.030 + 0.025*taper_profile(x))*(1 - 0.25*np.exp(-((x-0.145)/0.035)**2)),
    height_fn=lambda x: 0.030 + 0.026*taper_profile(x) + 0.016*np.exp(-((x+0.105)/0.045)**2),
    material=mat_upper)
# squash hidden lower portion slightly by clipping? keep tube
add_mesh(upper,'CABEDAL', mat_upper)

# Top opening dark oval and collar ring
opening = trimesh.creation.uv_sphere(segments=48, ring_count=16, radius=1.0)
opening.apply_scale([0.060,0.006,0.036])
opening.apply_translation([-0.055,0.106,0.0])
add_mesh(opening,'ABERTURA_INTERNA_ESCURA', mat_dark)

collar = trimesh.creation.torus(major_radius=0.042, minor_radius=0.003, major_segments=72, minor_segments=8)
# torus lies in XY around Z? rotate to x-z plane at top: default torus axis z, ring in XY. Want ring in XZ so rotate 90 about X.
collar.apply_transform(rotation_matrix(np.pi/2,[1,0,0]))
collar.apply_scale([1.3,1.0,0.8])
collar.apply_translation([-0.055,0.108,0.0])
add_mesh(collar,'COLAR_ABERTURA', mat_lace)

# Tongue
ling = trimesh.creation.box(extents=[0.075,0.010,0.034])
ling.apply_transform(rotation_matrix(np.deg2rad(-14), [0,0,1]))
ling.apply_translation([0.005,0.110,0.0])
add_mesh(ling,'LINGUETA', mat_lace)

# Rear pull tab
pull = trimesh.creation.box(extents=[0.015,0.060,0.009])
pull.apply_transform(rotation_matrix(np.deg2rad(8), [0,0,1]))
pull.apply_translation([-0.146,0.112,0.0])
add_mesh(pull,'PUXADOR_TRASEIRO', mat_lace)

# Contraforte heel reinforcement
heel = trimesh.creation.uv_sphere(segments=32, ring_count=16, radius=1)
heel.apply_scale([0.040,0.035,0.052])
heel.apply_translation([-0.135,0.065,0.0])
add_mesh(heel,'CONTRAFORTE', mat_upper)

# Side overlays (dark red swoops) as cylinder path segments

def cylinder_between(p1,p2,radius,mat,name,sections=16):
    p1=np.array(p1); p2=np.array(p2); v=p2-p1
    length=float(np.linalg.norm(v))
    if length < 1e-6: return None
    cyl=trimesh.creation.cylinder(radius=radius, height=length, sections=sections)
    # default cylinder along z, align to vector
    T=trimesh.geometry.align_vectors([0,0,1], v/length)
    cyl.apply_transform(T)
    cyl.apply_translation((p1+p2)/2)
    add_mesh(cyl,name,mat)
    return cyl

# Decorative side wave on lateral side (z+)
paths = [
    [(-0.120,0.060,0.057), (-0.070,0.083,0.061), (-0.020,0.075,0.062), (0.050,0.095,0.055)],
    [(-0.030,0.047,0.059), (0.035,0.052,0.061), (0.110,0.047,0.052)]
]
idx=0
for path in paths:
    for a,b in zip(path,path[1:]):
        cylinder_between(a,b,0.0045,mat_dark,f'DETALHE_LATERAL_{idx}',12); idx+=1
# inner side wave (z-)
for path in [[(-0.120,0.058,-0.057), (-0.050,0.080,-0.060), (0.040,0.074,-0.060), (0.120,0.055,-0.050)]]:
    for a,b in zip(path,path[1:]):
        cylinder_between(a,b,0.0038,mat_dark,f'DETALHE_INTERNO_{idx}',12); idx+=1

# Laces (crossing cylinders on top)
lace_xs=[-0.035,-0.015,0.005,0.025,0.045]
for k,x in enumerate(lace_xs):
    y=0.118 - abs(x)*0.08
    cylinder_between([x-0.017,y, -0.027],[x+0.018,y+0.004,0.027],0.0035,mat_lace,f'CADARCO_CRUZ_A_{k}',12)
    cylinder_between([x-0.017,y, 0.027],[x+0.018,y+0.004,-0.027],0.0035,mat_lace,f'CADARCO_CRUZ_B_{k}',12)
# lace knots loops
loop1=trimesh.creation.torus(major_radius=0.018, minor_radius=0.0022, major_segments=32, minor_segments=8)
loop1.apply_transform(rotation_matrix(np.pi/2,[1,0,0])); loop1.apply_scale([1.4,1,0.5]); loop1.apply_translation([0.050,0.120,0.022]); add_mesh(loop1,'CADARCO_LOOP_DIREITO',mat_lace)
loop2=loop1.copy(); loop2.apply_translation([0,0,-0.044]); add_mesh(loop2,'CADARCO_LOOP_ESQUERDO',mat_lace)
# Group placeholder named CADARCOS (tiny hidden-ish body) to satisfy object
cad_placeholder=trimesh.creation.uv_sphere(segments=8, ring_count=4, radius=0.001)
cad_placeholder.apply_translation([0.01,0.12,0])
add_mesh(cad_placeholder,'CADARCOS',mat_lace)

# Perforation dots/mesh texture as dark tiny disks on top and sides
for i,x in enumerate(np.linspace(-0.02,0.135,12)):
    width=0.017 + 0.028*taper_profile(x)
    for j,z in enumerate(np.linspace(-width*0.65,width*0.65,5)):
        if abs(z) > width*0.72: continue
        y=0.102 - 0.17*(x-0.02)**2 + 0.004*np.cos(j)
        dot=trimesh.creation.cylinder(radius=0.0014, height=0.0012, sections=8)
        dot.apply_transform(rotation_matrix(np.pi/2,[1,0,0]))
        dot.apply_translation([x,y,z])
        add_mesh(dot,f'FURINHO_MALHA_{i}_{j}',mat_dark)

# Sole tread details bottom
count=0
for x in np.linspace(-0.13,0.14,10):
    width=0.030+0.025*taper_profile(x)
    for z in np.linspace(-width*0.85,width*0.85,4):
        tread=trimesh.creation.box(extents=[0.017,0.005,0.010])
        tread.apply_transform(rotation_matrix(np.deg2rad((count%3-1)*18), [0,1,0]))
        tread.apply_translation([x,-0.033,z])
        add_mesh(tread,f'TRAVA_SOLADO_{count}',mat_out)
        count+=1
# placeholder detalhes solado
placeholder=trimesh.creation.uv_sphere(segments=8, ring_count=4, radius=0.001)
placeholder.apply_translation([0,-0.035,0])
add_mesh(placeholder,'DETALHES_SOLADO',mat_out)

# Simple 3D block letters for CORRE on lateral side z positive
# Letters are made of small white bars on the side plane, raised out of the shoe.
def add_bar(name, cx, cy, sx, sy, z=0.064, depth=0.004):
    b=trimesh.creation.box(extents=[sx, sy, depth])
    b.apply_translation([cx, cy, z])
    add_mesh(b,name,mat_logo)
    return b
letter_y=0.078
letter_h=0.030
bar=0.0045
start_x=-0.105
spacing=0.020
# Use segment patterns in local coordinates for block font
# Each letter width 0.015
patterns={
 'C': [('h',0,0.5),('h',0,-0.5),('v',-0.5,0)],
 'O': [('h',0,0.5),('h',0,-0.5),('v',-0.5,0),('v',0.5,0)],
 'R': [('v',-0.5,0),('h',0,0.5),('h',0,0.05),('v',0.5,0.28),('d',0.25,-0.28)],
 'E': [('v',-0.5,0),('h',0,0.5),('h',0,0),('h',0,-0.5)]
}
word='CORRE'
for li,ch in enumerate(word):
    lx=start_x+li*spacing
    for si,seg in enumerate(patterns[ch]):
        typ,a,b=seg
        if typ=='h':
            add_bar(f'LOGO_CORRE_{ch}_{li}_{si}', lx, letter_y + b*letter_h, 0.015, bar)
        elif typ=='v':
            add_bar(f'LOGO_CORRE_{ch}_{li}_{si}', lx + a*0.015, letter_y, bar, letter_h)
        elif typ=='d':
            # diagonal as cylinder on side
            p1=[lx, letter_y, 0.064]
            p2=[lx+0.010, letter_y-0.014,0.064]
            cylinder_between(p1,p2,0.0025,mat_logo,f'LOGO_CORRE_{ch}_{li}_{si}',8)
# LOGO_CORRE parent-ish placeholder
logo_placeholder=trimesh.creation.uv_sphere(segments=8, ring_count=4, radius=0.001)
logo_placeholder.apply_translation([-0.065,0.078,0.066])
add_mesh(logo_placeholder,'LOGO_CORRE',mat_logo)

# Tongue small logo/label and rear label
label=trimesh.creation.box(extents=[0.030,0.014,0.003])
label.apply_translation([0.012,0.127,0.0])
add_mesh(label,'ETIQUETA_LINGUETA_CORRE4',mat_logo)
# olympikus rear white strip
rear=trimesh.creation.box(extents=[0.008,0.038,0.003])
rear.apply_translation([-0.153,0.112,0.004])
add_mesh(rear,'ETIQUETA_OLYMPIKUS',mat_logo)

# Anchors as tiny invisible-ish spheres at required positions
anchors={
 'FOOT_ANCHOR':[0,0.060,0],
 'TOE_ANCHOR':[0.145,0.030,0],
 'HEEL_ANCHOR':[-0.135,0.030,0],
 'SOLE_CENTER':[0,0.000,0],
 'ANKLE_GUIDE':[-0.105,0.110,0],
 'INSTEP_GUIDE':[0.020,0.092,0]
}
for name,pos in anchors.items():
    s=trimesh.creation.uv_sphere(segments=8, ring_count=4, radius=0.001)
    s.apply_translation(pos)
    add_mesh(s,name,mat_anchor)

# Add root transform node? Trimesh scene nodes already flat. Add a tiny invisible root named Olympikus_Corre_4 maybe
root=trimesh.creation.uv_sphere(segments=8, ring_count=4, radius=0.001)
root.apply_translation([0,0,0])
add_mesh(root,'Olympikus_Corre_4',mat_anchor)

# Set camera view
scene.camera = trimesh.scene.Camera(resolution=(1200,800), fov=(45,45))
scene.camera_transform = trimesh.transformations.translation_matrix([0.45,0.25,0.55]) @ trimesh.transformations.rotation_matrix(np.deg2rad(65), [0,1,0])

# Export
out='/home/oai/share/corre4.glb'
scene.export(out)
print(out)
