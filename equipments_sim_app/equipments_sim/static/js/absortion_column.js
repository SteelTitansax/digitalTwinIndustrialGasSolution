document.addEventListener('DOMContentLoaded', function () {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5);

    const container = document.getElementById('absortionColumn');

    const camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        2000
    );
    camera.position.set(15, 12, 18); // alejada un poco más para ver la columna completa
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // MATERIALES
    const grayMaterial = new THREE.MeshStandardMaterial({ color: 0xaaaaaa, metalness: 0.6, roughness: 0.3 });
    const blueFlangeMaterial = new THREE.MeshStandardMaterial({ color: 0x2e5a88, metalness: 0.4, roughness: 0.6 });

    // DIMENSIONES (doble del anterior)
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
    topNozzle.position.y = mainHeight / 2 + 2.4 / 2 + 0.1;

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

    // BOQUILLAS LATERALES
    function createNozzle(yPosition) {
        const pipe = new THREE.Mesh(
            new THREE.CylinderGeometry(1.2, 1.2, 4.8, 32),
            grayMaterial
        );
        pipe.rotation.z = Math.PI / 2;
        pipe.position.set(mainRadius + 2.4, yPosition, 0);

        const flange = new THREE.Mesh(
            new THREE.CylinderGeometry(2.0, 2.0, 0.4, 32),
            blueFlangeMaterial
        );
        flange.rotation.z = Math.PI / 2;
        flange.position.set(mainRadius + 4.8, yPosition, 0);

        return [pipe, flange];
    }

    // MÁS SEPARADAS (doble)
    const [nozzle1, flange1] = createNozzle(7);
    const [nozzle2, flange2] = createNozzle(-7);

    // AGRUPAR COMPONENTES
    const columnGroup = new THREE.Group();
    columnGroup.add(
        cylinder, dome, topNozzle, topFlange,
        bottomCylinder, baseFlange,
        nozzle1, flange1,
        nozzle2, flange2
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