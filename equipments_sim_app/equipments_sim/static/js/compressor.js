document.addEventListener('DOMContentLoaded', function () {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5f5f5);

    const container = document.getElementById('compressor');

    const camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        2000
    );
    camera.position.set(18, 14, 22);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // === MATERIALES ===
    const grayMaterial = new THREE.MeshStandardMaterial({ color: 0xaaaaaa, metalness: 0.7, roughness: 0.3 });
    const blueFlangeMaterial = new THREE.MeshStandardMaterial({ color: 0x2e5a88, metalness: 0.5, roughness: 0.6 });
    const impellerMaterial = new THREE.MeshStandardMaterial({ color: 0xff6600, metalness: 0.6, roughness: 0.4 });

    // === COMPRESOR ===
    const compressorGroup = new THREE.Group();

    // Cuerpo principal (cilindro horizontal)
    const bodyLength = 4.5;
    const body = new THREE.Mesh(
        new THREE.CylinderGeometry(6, 6, bodyLength, 64),
        grayMaterial
    );
    body.rotation.z = Math.PI / 2;
    compressorGroup.add(body);

    // Entrada (boquilla frontal)
    const inlet = new THREE.Mesh(
        new THREE.CylinderGeometry(2.5, 2.5, 1.5, 32),
        grayMaterial
    );
    inlet.rotation.z = Math.PI / 2;
    inlet.position.x = -(bodyLength / 2 + 1.5 / 2);
    compressorGroup.add(inlet);

    // Flange frontal (azul) COMPACTO
    const inletFlange = new THREE.Mesh(
        new THREE.CylinderGeometry(3.5, 3.5, 0.6, 32),
        blueFlangeMaterial
    );
    inletFlange.rotation.z = Math.PI / 2;
    inletFlange.position.x = inlet.position.x - (1.5 / 2 + 0.6 / 2);
    compressorGroup.add(inletFlange);


    // Eje central reducido (misma longitud que el cuerpo)
    const shaft = new THREE.Mesh(
        new THREE.CylinderGeometry(0.6, 0.6, bodyLength, 32),
        grayMaterial
    );
    shaft.rotation.z = Math.PI / 2;
    compressorGroup.add(shaft);

    // Impeller (disco con paletas)
    const impeller = new THREE.Group();

    const disc = new THREE.Mesh(
        new THREE.CylinderGeometry(4, 4, 0.6, 32),
        impellerMaterial
    );
    disc.rotation.z = Math.PI / 2;
    impeller.add(disc);

    for (let i = 0; i < 6; i++) {
        const blade = new THREE.Mesh(
            new THREE.BoxGeometry(0.3, 3.5, 1),
            impellerMaterial
        );
        blade.position.y = 1.8;
        blade.rotation.z = (i * Math.PI) / 3;
        impeller.add(blade);
    }

    // centrado dentro del cuerpo
    impeller.position.x = 0;
    compressorGroup.add(impeller);

    scene.add(compressorGroup);

    // === ILUMINACIÓN ===
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 1.2);
    pointLight.position.set(30, 30, 30);
    scene.add(pointLight);

    // === ANIMACIÓN ===
    function animate() {
        requestAnimationFrame(animate);
        compressorGroup.rotation.y += 0.01;
        impeller.rotation.x += 0.1;
        renderer.render(scene, camera);
    }
    animate();

    // === AJUSTE AL REDIMENSIONAR ===
    window.addEventListener('resize', () => {
        const width = container.clientWidth;
        const height = container.clientHeight;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    });
});
