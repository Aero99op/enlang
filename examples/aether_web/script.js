document.addEventListener('DOMContentLoaded', () => {
  /* --- Interactive Canvas Particle Background --- */
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let width, height;
  let particles = [];
  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();
  class Particle {
    constructor() {
      this.reset();
    }
    reset() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.4;
      this.vy = (Math.random() - 0.5) * 0.4;
      this.radius = Math.random() * 1.5 + 0.5;
      this.alpha = Math.random() * 0.5 + 0.2;
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      if (this.x < 0 || this.x > width) this.vx *= -1;
      if (this.y < 0 || this.y > height) this.vy *= -1;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(100, 255, 218, ${this.alpha})`;
      ctx.fill();
    }
  }
  // Create particle pool
  const particleCount = Math.floor((width * height) / 15000);
  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }
  // Mouse interactivity
  let mouse = { x: null, y: null };
  window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });
  function render() {
    ctx.clearRect(0, 0, width, height);
    particles.forEach((p, index) => {
      p.update();
      p.draw();
      // Connect nearby particles with faint lines
      for (let j = index + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(100, 255, 218, ${0.15 * (1 - dist / 120)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    });
    requestAnimationFrame(render);
  }
  render();
  /* --- Stat Counter Scroll Animation --- */
  const statNumbers = document.querySelectorAll('.stat-number');
  let animated = false;
  function animateStats() {
    statNumbers.forEach((stat) => {
      const target = +stat.getAttribute('data-target');
      let count = 0;
      const speed = target / 50;
      const updateCount = () => {
        count += speed;
        if (count < target) {
          stat.innerText = count.toFixed(target % 1 !== 0 ? 1 : 0);
          setTimeout(updateCount, 30);
        } else {
          stat.innerText = target;
        }
      };
      updateCount();
    });
  }
  // Trigger stat count-up when section comes into viewport
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !animated) {
          animateStats();
          animated = true;
        }
      });
    },
    { threshold: 0.5 }
  );
  const statsSection = document.querySelector('.stats-section');
  if (statsSection) observer.observe(statsSection);
});
