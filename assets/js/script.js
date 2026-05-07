// ===== LOADING =====
window.addEventListener('load', () => {
  setTimeout(() => {
    document.getElementById('loading').classList.add('hidden');
    initReveal();
  }, 1400);
});

// ===== CANVAS PARTICLES =====
const canvas = document.getElementById('canvas-bg');
const ctx = canvas.getContext('2d');
let particles = [];
let W, H;

function resize() {
  W = canvas.width = window.innerWidth;
  H = canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

class Particle {
  constructor() { this.reset(); }
  reset() {
    this.x = Math.random() * W;
    this.y = Math.random() * H;
    this.vx = (Math.random() - 0.5) * 0.3;
    this.vy = (Math.random() - 0.5) * 0.3;
    this.r = Math.random() * 1.5 + 0.3;
    this.alpha = Math.random() * 0.5 + 0.1;
  }
  update() {
    this.x += this.vx;
    this.y += this.vy;
    if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(59,130,246,${this.alpha})`;
    ctx.fill();
  }
}

for (let i = 0; i < 80; i++) particles.push(new Particle());

function drawLines() {
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < 100) {
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.strokeStyle = `rgba(59,130,246,${0.06 * (1 - dist/100)})`;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }
}

function animate() {
  ctx.clearRect(0, 0, W, H);
  particles.forEach(p => { p.update(); p.draw(); });
  drawLines();
  requestAnimationFrame(animate);
}
animate();

// ===== CUSTOM CURSOR =====
const cursor = document.getElementById('cursor');
const trail = document.getElementById('cursorTrail');
let mx = 0, my = 0, tx = 0, ty = 0;

document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  cursor.style.left = mx - 4 + 'px';
  cursor.style.top = my - 4 + 'px';
});

function animCursor() {
  tx += (mx - tx) * 0.12;
  ty += (my - ty) * 0.12;
  trail.style.left = tx - 14 + 'px';
  trail.style.top = ty - 14 + 'px';
  requestAnimationFrame(animCursor);
}
animCursor();

document.querySelectorAll('a,button,.service-card,.stat-card,.project-card').forEach(el => {
  el.addEventListener('mouseenter', () => {
    cursor.style.transform = 'scale(2.5)';
    trail.style.transform = 'scale(1.5)';
    trail.style.borderColor = 'rgba(59,130,246,0.7)';
  });
  el.addEventListener('mouseleave', () => {
    cursor.style.transform = 'scale(1)';
    trail.style.transform = 'scale(1)';
    trail.style.borderColor = 'rgba(59,130,246,0.4)';
  });
});

// ===== SIDEBAR TOGGLE (MOBILE) =====
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebarExtra = document.getElementById('sidebarExtra');
sidebarToggle?.addEventListener('click', () => {
  sidebarExtra.classList.toggle('open');
  sidebarToggle.querySelector('span:last-child').textContent =
    sidebarExtra.classList.contains('open') ? '▴' : '▾';
});

// Auto-show sidebar content on desktop
if (window.innerWidth > 900) sidebarExtra.classList.add('open');

// ===== TAB NAVIGATION =====
const navBtns = document.querySelectorAll('[data-nav-link]');
const pages = document.querySelectorAll('[data-page]');

navBtns.forEach(btn => {
  btn.addEventListener('click', function() {
    navBtns.forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const target = this.dataset.pageTarget;
    pages.forEach(p => {
      if (p.dataset.page === target) {
        p.classList.add('active');
        // Re-trigger reveal animations
        setTimeout(() => {
          p.querySelectorAll('.reveal').forEach((el, i) => {
            el.classList.remove('visible');
            setTimeout(() => el.classList.add('visible'), i * 80);
          });
        }, 50);
      } else {
        p.classList.remove('active');
      }
    });
  });
});

// ===== SCROLL REVEAL =====
function initReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

  document.querySelectorAll('.reveal').forEach((el, i) => {
    el.style.transitionDelay = (i % 8) * 0.07 + 's';
    observer.observe(el);
  });
}

// ===== FORM =====
const formInputs = document.querySelectorAll('[data-form-input]');
const formBtn = document.querySelector('[data-form-btn]');

formInputs.forEach(input => {
  input.addEventListener('input', () => {
    const allFilled = [...formInputs].every(i => i.value.trim() !== '');
    formBtn.disabled = !allFilled;
  });
});

document.getElementById('contactForm')?.addEventListener('submit', e => {
  e.preventDefault();
  e.target.reset();
  formBtn.disabled = true;
  const toast = document.getElementById('toast');
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3500);
});

// ===== STAGGER CARDS ON LOAD =====
window.addEventListener('load', () => {
  setTimeout(() => {
    document.querySelectorAll('.page.active .reveal').forEach((el, i) => {
      setTimeout(() => el.classList.add('visible'), 200 + i * 100);
    });
  }, 1600);
});