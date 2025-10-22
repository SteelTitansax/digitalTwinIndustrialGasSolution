// 3D models IndSim app  
// -----------------------------------------------------------------------------------------------
// Author : Manuel Portero Leiva 
// -----------------------------------------------------------------------------------------------
// Purpose : Distillator column 3d Renderization, part of the IndSim front-end.
// ----------------------------------------------------------------------------------------------- 

document.addEventListener('DOMContentLoaded', function () {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5);

    const container = document.getElementById('distillationColumn');

    const camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        2000
    );
    camera.position.set(15, 12, 18);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // MATERIALES
    const grayMaterial = new THREE.MeshStandardMaterial({ color: 0xaaaaaa, metalness: 0.6, roughness: 0.3 });
    const blueFlangeMaterial = new THREE.MeshStandardMaterial({ color: 0x2e5a88, metalness: 0.4, roughness: 0.6 });

    // DIMENSIONES
    const mainRadius = 4;
    const mainHeight = 20;

    // CUERPO PRINCIPAL
    const cylinder = new THREE.Mesh(
        new THREE.CylinderGeometry(mainRadius, mainRadius, mainHeight, 64),
        grayMaterial
    );

    // TAPA SUPERIOR (semiesfera + boquilla)
    const dome = new THREE.Mesh(
        new THREE.SphereGeometry(mainRadius, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2),
        grayMaterial
    );
    dome.position.y = mainHeight / 2;

    const topNozzle = new THREE.Mesh(
        new THREE.CylinderGeometry(0.8, 0.8, 2.4, 32),
        grayMaterial
    );
    topNozzle.position.y = mainHeight / 2 + 1.2 + 0.1;

    // FLANGE SUPERIOR
    const topFlange = new THREE.Mesh(
        new THREE.CylinderGeometry(5.2, 5.2, 0.4, 32),
        blueFlangeMaterial
    );
    topFlange.position.y = mainHeight / 2 + 0.2;

    // BASE INFERIOR CON FLANGE
    const bottomCylinder = new THREE.Mesh(
        new THREE.CylinderGeometry(2.4, 2.4, 1.6, 32),
        grayMaterial
    );
    bottomCylinder.position.y = -mainHeight / 2 - 0.8;

    const baseFlange = new THREE.Mesh(
        new THREE.CylinderGeometry(5.2, 5.2, 0.4, 32),
        blueFlangeMaterial
    );
    baseFlange.position.y = -mainHeight / 2 - 1.6;

    // FUNCION PARA CREAR BOQUILLAS LATERALES
    function createNozzle(yPosition, angle = 0) {
        const pipe = new THREE.Mesh(
            new THREE.CylinderGeometry(1.2, 1.2, 4.8, 32),
            grayMaterial
        );
        pipe.rotation.z = Math.PI / 2;
        pipe.rotation.y = angle;
        pipe.position.set((mainRadius + 2.4) * Math.cos(angle), yPosition, (mainRadius + 2.4) * Math.sin(angle));

        const flange = new THREE.Mesh(
            new THREE.CylinderGeometry(2.0, 2.0, 0.4, 32),
            blueFlangeMaterial
        );
        flange.rotation.z = Math.PI / 2;
        flange.rotation.y = angle;
        flange.position.set((mainRadius + 4.8) * Math.cos(angle), yPosition, (mainRadius + 4.8) * Math.sin(angle));

        return [pipe, flange];
    }

    // BOQUILLAS
    const [nozzle1, flange1] = createNozzle(7, 0);
    const [nozzle2, flange2] = createNozzle(-7, 0);
    const [nozzle3, flange3] = createNozzle(0, 0);
    const [nozzle4, flange4] = createNozzle(-7, Math.PI); // en sentido opuesto entre las dos inferiores

    // AGRUPAR COMPONENTES
    const columnGroup = new THREE.Group();
    columnGroup.add(
        cylinder, dome, topNozzle, topFlange,
        bottomCylinder, baseFlange,
        nozzle1, flange1,
        nozzle2, flange2,
        nozzle3, flange3,
        nozzle4, flange4
    );

    scene.add(columnGroup);

    // ILUMINACIÓN
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 1.2);
    pointLight.position.set(30, 30, 30);
    scene.add(pointLight);

    // ANIMACIÓN
    function animate() {
        requestAnimationFrame(animate);
        columnGroup.rotation.y += 0.01;
        renderer.render(scene, camera);
    }
    animate();

    // AJUSTE AL REDIMENSIONAR
    window.addEventListener('resize', () => {
        const width = container.clientWidth;
        const height = container.clientHeight;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    });
});
