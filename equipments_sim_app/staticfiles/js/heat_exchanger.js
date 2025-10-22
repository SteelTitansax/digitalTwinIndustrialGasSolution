// 3D models IndSim app  
// -----------------------------------------------------------------------------------------------
// Author : Manuel Portero Leiva 
// -----------------------------------------------------------------------------------------------
// Purpose : Heat exchanger 3d Renderization, part of the IndSim front-end.
// ----------------------------------------------------------------------------------------------- 

document.addEventListener('DOMContentLoaded', function () {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5);

    const container = document.getElementById('heatExchanger');

    const camera = new THREE.PerspectiveCamera(
        65,
        container.clientWidth / container.clientHeight,
        0.1,
        2000
    );
    camera.position.set(18, 14, 20);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // MATERIALES
    const metalMaterial = new THREE.MeshStandardMaterial({
        color: 0xb0b0b0,
        metalness: 0.8,
        roughness: 0.3
    });
    const flangeMaterial = new THREE.MeshStandardMaterial({
        color: 0x4b6a88,
        metalness: 0.5,
        roughness: 0.6
    });
    const internalMaterial = new THREE.MeshStandardMaterial({
        color: 0x999999,
        metalness: 0.6,
        roughness: 0.5
    });

    // DIMENSIONES GENERALES
    const shellRadius = 3.2;
    const shellHeight = 18;

    // CARCASA PRINCIPAL
    const shell = new THREE.Mesh(
        new THREE.CylinderGeometry(shellRadius, shellRadius, shellHeight, 64, 1, true),
        metalMaterial
    );

    // TAPAS
    const topHead = new THREE.Mesh(
        new THREE.SphereGeometry(shellRadius, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2),
        metalMaterial
    );
    topHead.position.y = shellHeight / 2;

    const bottomHead = new THREE.Mesh(
        new THREE.SphereGeometry(shellRadius, 32, 16, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2),
        metalMaterial
    );
    bottomHead.position.y = -shellHeight / 2;

    // BASE INFERIOR CON FLANGE
    const baseCylinder = new THREE.Mesh(
        new THREE.CylinderGeometry(1.8, 1.8, 1.6, 32),
        metalMaterial
    );
    baseCylinder.position.y = -shellHeight / 2 - 0.8;

    const baseFlange = new THREE.Mesh(
        new THREE.CylinderGeometry(4.2, 4.2, 0.4, 32),
        flangeMaterial
    );
    baseFlange.position.y = -shellHeight / 2 - 1.6;

    // TAPA SUPERIOR CON BOQUILLA
    const topNozzle = new THREE.Mesh(
        new THREE.CylinderGeometry(0.7, 0.7, 2.4, 32),
        metalMaterial
    );
    topNozzle.position.y = shellHeight / 2 + 2.4 / 2;

    const topFlange = new THREE.Mesh(
        new THREE.CylinderGeometry(1.6, 1.6, 0.3, 32),
        flangeMaterial
    );
    topFlange.position.y = shellHeight / 2 + 1.3;

    // FUNCIÓN PARA CREAR BOQUILLAS LATERALES
    function createSideNozzle(yPosition) {
        const pipe = new THREE.Mesh(
            new THREE.CylinderGeometry(0.8, 0.8, 4, 32),
            metalMaterial
        );
        pipe.rotation.z = Math.PI / 2;
        pipe.position.set(shellRadius + 2, yPosition, 0);

        const flange = new THREE.Mesh(
            new THREE.CylinderGeometry(1.5, 1.5, 0.3, 32),
            flangeMaterial
        );
        flange.rotation.z = Math.PI / 2;
        flange.position.set(shellRadius + 3.8, yPosition, 0);

        return [pipe, flange];
    }

    // BOQUILLAS
    const [inletPipe, inletFlange] = createSideNozzle(-7);
    const [coolPipe, coolFlange] = createSideNozzle(-1);
    const [hotPipe, hotFlange] = createSideNozzle(6);

    // TUBOS INTERNOS (SIMULACIÓN DE HAZ DE TUBOS)
    const tubeGroup = new THREE.Group();
    const nTubes = 12;
    const nLevels = 5;
    const tubeRadius = 0.15;
    const tubeLength = 5.5;

    for (let level = 0; level < nLevels; level++) {
        const y = -6 + level * 3;
        for (let i = 0; i < nTubes; i++) {
            const angle = (i / nTubes) * Math.PI * 2;
            const r = 1.6;
            const x = Math.cos(angle) * r;
            const z = Math.sin(angle) * r;
            const tube = new THREE.Mesh(
                new THREE.CylinderGeometry(tubeRadius, tubeRadius, tubeLength, 16),
                internalMaterial
            );
            tube.rotation.x = Math.PI / 2;
            tube.position.set(x, y, 0);
            tubeGroup.add(tube);
        }
    }

    // AGRUPAR TODO
    const exchangerGroup = new THREE.Group();
    exchangerGroup.add(
        shell, topHead, bottomHead,
        baseCylinder, baseFlange,
        topNozzle, topFlange,
        inletPipe, inletFlange,
        coolPipe, coolFlange,
        hotPipe, hotFlange,
        tubeGroup
    );

    scene.add(exchangerGroup);

    // ILUMINACIÓN
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 1.3);
    pointLight.position.set(25, 25, 25);
    scene.add(pointLight);

    // ANIMACIÓN
    function animate() {
        requestAnimationFrame(animate);
        exchangerGroup.rotation.y += 0.008;
        renderer.render(scene, camera);
    }
    animate();

    // RESPONSIVE
    window.addEventListener('resize', () => {
        const width = container.clientWidth;
        const height = container.clientHeight;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    });
});
