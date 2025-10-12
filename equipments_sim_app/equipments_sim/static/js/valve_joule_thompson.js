document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('valveJouleThompson');
    if (!container) {
        console.error('No existe el contenedor con id "valveGate"');
        return;
    }

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    const camera = new THREE.PerspectiveCamera(
        60,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );
    camera.position.set(15, 10, 20);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // === MATERIALES ===
    const metal = new THREE.MeshStandardMaterial({ color: 0x999999, metalness: 0.8, roughness: 0.3 });
    const wheelMat = new THREE.MeshStandardMaterial({ color: 0x336699, metalness: 0.5, roughness: 0.6 });

    const valveGroup = new THREE.Group();

    // === CUERPO HORIZONTAL ===
    const body = new THREE.Mesh(
        new THREE.CylinderGeometry(3, 3, 12, 32),
        metal
    );
    body.rotation.z = Math.PI / 2;
    valveGroup.add(body);


    // === PUERTA SIMPLE ===
    const gate = new THREE.Mesh(
        new THREE.BoxGeometry(0.25, 3, 3),
        metal
    );
    gate.position.set(0, 0, 0);
    valveGroup.add(gate);

    // === VÁSTAGO ===
    const stem = new THREE.Mesh(
        new THREE.CylinderGeometry(0.4, 1.3, 5.8, 8),
        metal
    );
    stem.position.set(0, 3, 0);
    valveGroup.add(stem);

    // === MANILLA SIMPLE ===
    const wheel = new THREE.Mesh(
        new THREE.TorusGeometry(2.5, 0.2, 16, 100),
        wheelMat
    );
    wheel.rotation.x = Math.PI / 2;
    wheel.position.set(0, 6, 0);
    valveGroup.add(wheel);

    scene.add(valveGroup);

    // === ILUMINACIÓN ===
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 1.2);
    pointLight.position.set(20, 20, 20);
    scene.add(pointLight);

    // === ANIMACIÓN ===
    function animate() {
        requestAnimationFrame(animate);
        valveGroup.rotation.y += 0.005;
        renderer.render(scene, camera);
    }
    animate();

    // === RESPONSIVE ===
    window.addEventListener('resize', () => {
        const width = container.clientWidth;
        const height = container.clientHeight;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    });
});
