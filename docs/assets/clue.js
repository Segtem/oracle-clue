(() => {
  'use strict';

  const $ = id => document.getElementById(id);
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');

  const stages = [
    {
      tool: "ORACLE-CLUE + GIT",
      maturity: "Disponible en 0.1.0a1",
      title: "1. Repositorio con árbol limpio",
      copy: "Clue opera sobre commits confirmados. Si hay diferencias en archivos versionados respecto de HEAD, Clue se detiene de inmediato para evitar mezclar cambios pendientes con los commits seleccionados.",
      input: "Repositorio Git local y referencia base (ej. HEAD~1)",
      output: "Archivos versionados sin diferencias con HEAD y hashes SHA de base y HEAD",
      decision: "Confirmar los cambios antes de revisar.",
      why: "El historial de Git es la fuente de verdad. El diff excluye archivos no versionados o ignorados. Si los elegís explícitamente con --contexto, pueden incluirse y se comprueba su huella.",
      tracker: "01 / Repositorio limpio y commits resueltos",
      actions: [
        { label: "¿Qué pasa con cambios sin commit?", type: "warn", msg: "CLUE: hay cambios versionados sin commit; confirmalos o usá un checkout limpio." },
        { label: "¿Y si la base no existe?", type: "warn", msg: "CLUE: Git no pudo completar rev-parse: fatal: Needed a single revision." },
        { label: "Archivos versionados sin diferencias con HEAD", type: "info", msg: "HEAD y base resueltos. Procediendo a examinar el diff." }
      ]
    },
    {
      tool: "ORACLE-CLUE PREPARAR",
      maturity: "Disponible en 0.1.0a1",
      title: "2. Extracción del diff y omisiones",
      copy: "Recolecta el diff raw de Git sin abreviar. Aplica límites estrictos: rechaza más de 200 archivos y blobs de más de 256 KB. Omite y declara binarios, enlaces simbólicos y rutas de credenciales conocidas (.env, .ssh, *.key).",
      input: "Commits base y HEAD en Git",
      output: "Diff unificado, rangos por lado y lista de omisiones",
      decision: "Revisar las omisiones declaradas.",
      why: "El filtro de nombres conocidos no garantiza ausencia de secretos en otros archivos. La persona a cargo debe inspeccionar qué entra al paquete.",
      tracker: "02 / Diff extraído (diff_sha256 calculado)",
      actions: [
        { label: "¿Qué pasa si hay un archivo .env?", type: "info", msg: "Se declara en omissions con razón: 'ruta de credenciales conocida'." },
        { label: "¿Si el diff supera 200 archivos?", type: "warn", msg: "CLUE: el cambio supera 200 archivos; dividí la revisión." },
        { label: "¿Y si un archivo supera 256 KB?", type: "warn", msg: "CLUE: archivo supera el límite de 256000 bytes; reducí el cambio." }
      ]
    },
    {
      tool: "ORACLE-CLUE PREPARAR",
      maturity: "Disponible en 0.1.0a1",
      title: "3. Archivos de contexto explícitos",
      copy: "Podés adjuntar especificaciones y evidencias mediante --contexto ruta. Clue comprueba que sean rutas relativas seguras dentro del repo, no sigan enlaces simbólicos y no superen 256 KB. Cada uno lleva su SHA-256.",
      input: "Rutas relativas dentro del repo (ej. spec.md)",
      output: "Archivos de contexto con su SHA-256 individual",
      decision: "Seleccionar solo el contexto relevante.",
      why: "Clue no envía datos a la red. Todo lo que incluyas formará parte del paquete para el revisor externo que elijas.",
      tracker: "03 / Contexto explícito adjuntado y hasheado",
      actions: [
        { label: "¿Qué pasa si intento leer un symlink?", type: "warn", msg: "CLUE: no se siguen enlaces simbólicos de contexto." },
        { label: "¿Si la ruta es absoluta o sale del repo?", type: "warn", msg: "CLUE: contexto debe ser una ruta relativa sin credenciales conocidas." },
        { label: "Contexto spec.md verificado", type: "info", msg: "Hash SHA-256 incorporado a la estructura canónica." }
      ]
    },
    {
      tool: "ORACLE-CLUE PREPARAR",
      maturity: "Disponible en 0.1.0a1",
      title: "4. Paquete reproducible",
      copy: "Serializa el paquete bajo schema oracle-clue.bundle/v1 y calcula context_sha256. Si elegís --salida, el archivo debe estar fuera del repo y ser nuevo; sin esa opción, el JSON sale por terminal. El límite del paquete compacto es 1 MB; el modo 'x' se aplica al archivo de salida.",
      input: "Diff, contextos, metadatos y omisiones",
      output: "Archivo nuevo contexto.json fuera del repo; sin --salida, JSON por terminal",
      decision: "Conservá el paquete usado para la revisión.",
      why: "Cambiar HEAD, archivos versionados o el contexto seleccionado exige renovar el paquete y la revisión. Los archivos no versionados o ignorados fuera del contexto seleccionado no se comprueban.",
      tracker: "04 / Paquete contexto.json preparado",
      actions: [
        { label: "¿Qué pasa si guardo dentro del repo?", type: "warn", msg: "CLUE: guardá el paquete fuera del repo revisado." },
        { label: "¿Y si el archivo de salida ya existe?", type: "warn", msg: "FileExistsError: Clue usa modo de creación exclusiva ('x') para no pisar paquetes previos." },
        { label: "Paquete guardado con éxito", type: "info", msg: "Paquete preparado: ../contexto.json; omisiones: 0. No es un informe de revisión." }
      ]
    },
    {
      tool: "REVISOR EXTERNO (PERSONA O IA)",
      maturity: "Externo a Clue · Adaptador IA futuro",
      title: "5. Revisión externa y hallazgos pendientes",
      copy: "Una persona o proveedor externo lee el paquete y produce informe.json conforme a hallazgos.schema.json. Todos los hallazgos deben tener status: 'pendiente'. Clue 0.1.0a1 no llama a modelos de IA.",
      input: "El paquete contexto.json",
      output: "informe.json con hallazgos exclusivamente 'pendiente'",
      decision: "Ningún modelo aprueba el cambio.",
      why: "El schema del informe rechaza estados como resuelto o descartado. Un informe vacío o incompleto nunca equivale a una aprobación.",
      tracker: "05 / Informe externo recibido (pendiente de validación)",
      actions: [
        { label: "¿Qué pasa si el modelo pone status: 'aprobado'?", type: "warn", msg: "ValidationError: 'aprobado' no cumple el schema. Solo se permite 'pendiente'." },
        { label: "¿Si el paquete tuvo omisiones y dice 'completo'?", type: "warn", msg: "CLUE: un paquete con omisiones exige un informe incompleto con limitaciones declaradas." },
        { label: "Informe con hallazgos pendientes", type: "info", msg: "Listo para verificación de correspondencia e integridad con Clue." }
      ]
    },
    {
      tool: "ORACLE-CLUE VALIDAR",
      maturity: "Disponible en 0.1.0a1",
      title: "6. Validación de formato y vigencia",
      copy: "oracle-clue validar re-recolecta el contexto del repositorio actual y exige coincidencia exacta con el paquete. Comprueba que las huellas coincidan y que los rangos de línea pertenezcan a los hunks del diff.",
      input: "informe.json + contexto.json + repo actual",
      output: "Resultado de formato y vigencia",
      decision: "Validar NO es aprobar.",
      why: "Clue comprueba los enlaces al contexto y que las ubicaciones estén dentro de los rangos, que incluyen líneas sin modificar. No juzga si el hallazgo es cierto ni certifica ausencia de bugs.",
      tracker: "06 / Formato y vigencia verificados",
      actions: [
        { label: "¿Qué pasa si el informe señala línea 999 (fuera del diff)?", type: "warn", msg: "CLUE: el rango del hallazgo no pertenece a ese lado del diff." },
        { label: "¿Si se modificó el código o el commit en Git?", type: "warn", msg: "CLUE: el paquete no coincide con el repositorio/contexto actual." },
        { label: "Informe coherente y vigente", type: "info", msg: "Formato y vigencia verificados. No confirma los hallazgos ni autentica al revisor o al actor humano." }
      ]
    },
    {
      tool: "PERSONA + ORACLE-CLUE",
      maturity: "Disponible en 0.1.0a1",
      title: "7. Decisiones humanas y registro de decisiones",
      copy: "Las decisiones humanas se guardan por separado en triage.json (triage.schema.json), enlazadas al hash exacto del informe. Cada decisión indica corregido, descartado o riesgo_aceptado con motivo y actor.",
      input: "triage.json con decisiones fechadas y motivadas",
      output: "Validación de referencias y decisiones no duplicadas",
      decision: "La responsabilidad final es humana.",
      why: "Clue comprueba que las decisiones correspondan al informe vigente. No autentica la identidad de quien firma ni ejecuta correcciones de código.",
      tracker: "07 / Registro verificado y vinculado al informe",
      actions: [
        { label: "¿Qué pasa si el triage apunta a otro informe?", type: "warn", msg: "CLUE: triage vinculado a otro informe (report_sha256 no coincide)." },
        { label: "¿Si una decisión no tiene motivo?", type: "warn", msg: "ValidationError: 'reason' es campo obligatorio en cada decisión." },
        { label: "Triage completo verificado", type: "info", msg: "Decisiones enlazadas por SHA-256 al informe verificado, sin autenticar identidades." }
      ]
    }
  ];

  let current = 0;
  let playing = false;
  let timer = null;
  let frame = null;
  let elapsed = 0;
  let lastTime = null;

  const canvas = $('clue-scene');
  const ctx = canvas ? canvas.getContext('2d') : null;

  // Paleta de colores pixel art coherente con el estilo de Factory/Task
  const palette = {
    bg: '#132421',
    wallGrid: '#1e3831',
    table: '#243b34',
    tableTop: '#325247',
    gridLines: '#416659',
    lampMetal: '#7a9187',
    lampGold: '#ebc36f',
    lightBeam: '#fff8d60e',
    paperBase: '#1a2e28',
    paperHead: '#1e3831',
    diffDelete: '#d46b5a',
    diffAdd: '#a2d6b5',
    diffText: '#789487',
    lensRing: '#ebc36f',
    lensGlass: '#467468',
    lensReflect: '#b5e2d6',
    folder: '#c7a97b',
    folderTab: '#9c7c4e',
    stampPending: '#ebc36f',
    stampValid: '#bceb8f',
    personSkin: '#e8b480',
    personHair: '#5c4130',
    personCoat: '#c5d9a9',
    personPants: '#27443c'
  };

  function updateView() {
    const s = stages[current];
    if ($('stage-tool')) $('stage-tool').textContent = s.tool;
    if ($('stage-maturity')) {
      $('stage-maturity').textContent = s.maturity;
      $('stage-maturity').className = 'maturity' + (s.maturity.includes('Externo') || s.maturity.includes('futuro') ? ' planned' : '');
    }
    if ($('stage-title')) $('stage-title').textContent = s.title;
    if ($('stage-copy')) $('stage-copy').textContent = s.copy;
    if ($('stage-input')) $('stage-input').textContent = s.input;
    if ($('stage-output')) $('stage-output').textContent = s.output;
    if ($('decision-title')) $('decision-title').textContent = s.decision;
    if ($('decision-copy')) $('decision-copy').textContent = s.why;
    if ($('tracker-status')) $('tracker-status').textContent = s.tracker;
    if ($('counter')) $('counter').textContent = `${String(current + 1).padStart(2, '0')} / 07`;

    // Botones de etapa
    document.querySelectorAll('.stations button').forEach((b, idx) => {
      if (idx === current) {
        b.setAttribute('aria-current', 'step');
      } else {
        b.removeAttribute('aria-current');
      }
    });

    // Acciones de decision
    const actionsContainer = $('decision-actions');
    const feedback = $('decision-feedback');
    if (actionsContainer && feedback) {
      actionsContainer.innerHTML = '';
      feedback.textContent = 'Seleccioná un caso de prueba para simular la respuesta de Clue:';
      feedback.className = '';
      s.actions.forEach(act => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'action-pill';
        btn.textContent = act.label;
        btn.addEventListener('click', () => {
          feedback.textContent = act.msg;
          feedback.className = act.type;
        });
        actionsContainer.appendChild(btn);
      });
    }

    // Controles de transporte
    if ($('previous')) $('previous').disabled = current === 0;
    if ($('next')) $('next').disabled = current === stages.length - 1;
    if ($('play')) {
      $('play').disabled = reduced.matches || current === stages.length - 1;
      $('play').setAttribute('aria-pressed', String(playing));
      if ($('play-icon')) $('play-icon').textContent = playing ? 'Ⅱ' : '▶';
      if ($('play-label')) $('play-label').textContent = playing ? 'Pausar' : 'Reproducir';
    }

    if ($('motion-status')) {
      if (reduced.matches) {
        $('motion-status').textContent = 'Movimiento reducido activado: navegá paso a paso.';
      } else if (playing) {
        $('motion-status').textContent = `Reproduciendo: etapa ${current + 1} de ${stages.length}.`;
      } else {
        $('motion-status').textContent = 'Pausa. Avanzá a tu ritmo o probá las simulaciones.';
      }
    }

    draw(elapsed);
  }

  function goTo(index) {
    if (index < 0 || index >= stages.length) return;
    current = index;
    updateView();
  }

  function stop() {
    playing = false;
    clearTimeout(timer);
    cancelAnimationFrame(frame);
    timer = frame = null;
    lastTime = null;
    updateView();
  }

  function start() {
    if (reduced.matches || current === stages.length - 1) return;
    clearTimeout(timer);
    cancelAnimationFrame(frame);
    lastTime = null;
    playing = true;
    updateView();
    frame = requestAnimationFrame(animate);
    timer = setTimeout(() => {
      if (current < stages.length - 1) {
        goTo(current + 1);
        start();
      } else {
        stop();
      }
    }, 4500);
  }

  function animate(now) {
    if (!playing || reduced.matches) return;
    if (lastTime !== null) elapsed += Math.min(now - lastTime, 80);
    lastTime = now;
    draw(elapsed);
    frame = requestAnimationFrame(animate);
  }

  // Pixel art canvas nativo
  function rect(x, y, w, h, color) {
    if (!ctx) return;
    ctx.fillStyle = color;
    ctx.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h));
  }

  function pixelLine(x, y, w, color) {
    rect(x, y, w, 2, color);
  }

  function pixelText(txt, x, y, color, size = 11, align = 'left') {
    if (!ctx) return;
    ctx.fillStyle = color;
    ctx.font = `${size}px ${palette.mono || 'monospace'}`;
    ctx.textAlign = align;
    ctx.fillText(txt, Math.round(x), Math.round(y));
  }

  function sprite(pattern, x, y, colors, scale = 2) {
    pattern.forEach((row, dy) => {
      [...row].forEach((p, dx) => {
        if (colors[p]) {
          rect(x + dx * scale, y + dy * scale, scale, scale, colors[p]);
        }
      });
    });
  }

  // Dibuja una figura pixel art de una persona analista/revisora
  function drawInspector(x, y, pose = 'stand') {
    // 9x11 sprite
    const pattern = pose === 'inspect' ? [
      '..hhhhh..',
      '.hhhhhhh.',
      '.sssssss.',
      '..sssss..',
      '..ccccc..',
      '.scccccs.',
      '.scccccl.',
      '..ccccc..',
      '..pp.pp..',
      '..pp.pp..',
      '..bb.bb..'
    ] : [
      '..hhhhh..',
      '.hhhhhhh.',
      '.sssssss.',
      '..sssss..',
      '..ccccc..',
      '.scccccs.',
      '.scccccs.',
      '..ccccc..',
      '..pp.pp..',
      '..pp.pp..',
      '.bbb.bbb.'
    ];

    sprite(pattern, x, y, {
      h: palette.personHair,
      s: palette.personSkin,
      c: palette.personCoat,
      p: palette.personPants,
      b: '#10201c',
      l: palette.lampGold
    }, 3);
  }

  // Dibuja la lupa de inspección de Clue
  function drawMagnifier(x, y, scale = 3) {
    const lens = [
      '....gggg....',
      '..gg....gg..',
      '.g........g.',
      '.g...rr...g.',
      '.g...rr...g.',
      '.g........g.',
      '..gg....gg..',
      '....ggggkk..',
      '.......kkkk.',
      '........kkkk',
      '.........kkk'
    ];
    sprite(lens, x, y, {
      g: palette.lensRing,
      r: palette.diffDelete,
      k: '#a67c43'
    }, scale);
  }

  // Dibuja un archivador de contexto con sello SHA
  function drawFolder(x, y, label = 'spec') {
    rect(x, y, 42, 32, palette.folderTab);
    rect(x + 2, y + 4, 38, 26, palette.folder);
    rect(x + 6, y + 8, 20, 2, '#87693d');
    rect(x + 6, y + 13, 28, 2, '#87693d');
    rect(x + 6, y + 18, 16, 2, '#87693d');
    // sello hash
    rect(x + 24, y + 20, 12, 8, '#326852');
    pixelText('#', x + 27, y + 27, '#a2d6b5', 8);
  }

  // Dibuja la escena principal
  function draw(t = 0) {
    if (!ctx) return;
    ctx.imageSmoothingEnabled = false;

    // Fondo del laboratorio / taller
    rect(0, 0, 1152, 380, palette.bg);

    // Cuadrícula de pared milimetrada tenue
    for (let x = 0; x < 1152; x += 32) {
      rect(x, 0, 1, 260, palette.wallGrid);
    }
    for (let y = 0; y < 260; y += 32) {
      rect(0, y, 1152, 1, palette.wallGrid);
    }

    // Estantería de fondo y tubos de cableado
    rect(0, 50, 1152, 4, '#203c34');
    rect(180, 20, 48, 30, '#1c332c');
    rect(185, 25, 38, 3, '#3c6657');
    pixelText('ORACLE CLUE 0.1.0a1', 190, 40, '#629381', 9);

    // Ménsulas de la mesa
    rect(80, 250, 992, 10, '#1b302a');

    // Superficie de la mesa de inspección milimetrada
    rect(70, 260, 1012, 110, palette.table);
    rect(70, 260, 1012, 8, palette.tableTop);
    for (let x = 90; x < 1070; x += 24) {
      rect(x, 260, 1, 6, palette.gridLines);
    }

    // Patas de la mesa
    rect(90, 270, 24, 110, '#162823');
    rect(1038, 270, 24, 110, '#162823');

    // 1. ZONA IZQUIERDA: Lámpara de inspección y árbol Git
    rect(120, 120, 8, 140, palette.lampMetal);
    rect(124, 100, 60, 6, palette.lampMetal);
    rect(170, 90, 30, 20, palette.lampGold);
    // Haz de luz cálido sobre el diff
    ctx.fillStyle = palette.lightBeam;
    ctx.beginPath();
    ctx.moveTo(185, 110);
    ctx.lineTo(130, 260);
    ctx.lineTo(440, 260);
    ctx.closePath();
    ctx.fill();

    // 2. EL COMPARADOR DE DIFF (Centro-Izquierda: x=220 a 540)
    // Rollo Base (HEAD~1)
    rect(230, 120, 130, 135, palette.paperBase);
    rect(230, 120, 130, 16, '#142520');
    pixelText('BASE (HEAD~1)', 240, 132, '#8ca89c', 9);
    // Líneas del código base
    for (let i = 0; i < 7; i++) {
      const ly = 146 + i * 14;
      if (i === 1) {
        // Línea que será borrada (-)
        rect(240, ly, 105, 10, '#3b2220');
        pixelLine(244, ly + 4, 80, palette.diffDelete);
        pixelText('-', 234, ly + 8, palette.diffDelete, 9);
      } else {
        pixelLine(244, ly + 4, 60 + (i * 13) % 40, palette.diffText);
      }
    }

    // Rollo Head (HEAD)
    rect(380, 120, 130, 135, palette.paperHead);
    rect(380, 120, 130, 16, '#183029');
    pixelText('HEAD (REVISADO)', 390, 132, palette.diffAdd, 9);
    // Líneas del código actual
    for (let i = 0; i < 7; i++) {
      const ly = 146 + i * 14;
      if (i === 1) {
        // Línea agregada (+) con defecto
        rect(390, ly, 105, 10, '#1c3d31');
        pixelLine(394, ly + 4, 80, palette.diffAdd);
        pixelText('+', 384, ly + 8, palette.diffAdd, 9);
      } else {
        pixelLine(394, ly + 4, 60 + (i * 13) % 40, palette.diffText);
      }
    }

    // 3. ARCHIVADORES DE CONTEXTO Y FILTRO DE SECRETOS (x=530 a 640)
    drawFolder(540, 200, 'spec');
    if (current >= 2) {
      drawFolder(555, 185, 'reglas');
    }
    // Filtro de credenciales (.env omitido)
    rect(600, 215, 24, 30, '#182d26');
    rect(602, 217, 20, 4, palette.diffDelete);
    pixelText('.env', 604, 234, '#c97869', 8);
    pixelText('OMITIDO', 594, 256, '#8fa89b', 8);

    // 4. PAQUETE CANÓNICO / BUNDLE (x=660 a 760)
    const boxColor = current >= 3 ? '#295447' : '#1c342d';
    rect(660, 175, 80, 70, boxColor);
    rect(660, 175, 80, 10, '#366d5c');
    pixelText('PAQUETE', 675, 195, '#dbebe3', 10);
    pixelText('contexto.json', 670, 210, palette.lampGold, 9);
    pixelText('diff_sha256', 670, 224, '#87aba0', 8);
    pixelText('context_sha256', 670, 235, '#87aba0', 8);

    // 5. INFORME EXTERNO (x=770 a 890)
    const repColor = current >= 4 ? '#f6f5ec' : '#334841';
    rect(770, 140, 105, 115, repColor);
    rect(770, 140, 105, 14, '#243b34');
    pixelText('informe.json', 778, 151, '#d5e8dc', 9);
    if (current >= 4) {
      pixelText('ID: HALLAZGO-01', 778, 170, '#182a25', 9);
      pixelText('kind: bug', 778, 183, '#182a25', 9);
      pixelText('línea: total.py:2', 778, 196, '#182a25', 9);
      // Sello status: pendiente
      rect(778, 208, 88, 16, '#f7edd2');
      rect(778, 208, 88, 1, palette.stampPending);
      rect(778, 223, 88, 1, palette.stampPending);
      pixelText('STATUS: PENDIENTE', 782, 220, '#855f13', 9);
      pixelText('verification: tests', 778, 238, '#4d6358', 8);
    }

    // 6. VALIDADOR CLUE Y SELLO DE INTEGRIDAD (x=895 a 970)
    rect(895, 180, 75, 65, '#1e3831');
    rect(895, 180, 75, 12, '#2b4f45');
    pixelText('VALIDADOR', 904, 190, '#cce3d8', 9);
    if (current >= 5) {
      rect(902, 205, 60, 24, '#2a5e44');
      pixelText('✓ VÁLIDO', 908, 221, palette.stampValid, 10);
      pixelText('No aprueba', 905, 238, '#94b3a4', 8);
    } else {
      pixelText('Esperando', 905, 218, '#5d7d71', 9);
    }

    // 7. LA PERSONA EN EL TRIAGE (x=990 a 1060)
    drawInspector(995, 160, current === 6 ? 'inspect' : 'stand');
    if (current === 6) {
      // Sello de registro de decisiones
      rect(980, 115, 95, 34, '#f2f8eb');
      rect(980, 115, 95, 2, '#38734e');
      pixelText('TRIAGE HUMANO', 986, 128, '#204d30', 9);
      pixelText('Decisión: CORREGIDO', 986, 142, '#204d30', 8);
    }

    // Dinámica según la etapa: posición de la LUPA
    let magnX = 350, magnY = 150;
    if (current === 0) {
      magnX = 220; magnY = 170;
    } else if (current === 1) {
      // La lupa enfoca el diff
      const bob = Math.sin(t / 250) * 4;
      magnX = 340; magnY = 145 + bob;
    } else if (current === 2) {
      magnX = 530; magnY = 170;
    } else if (current === 3) {
      magnX = 660; magnY = 160;
    } else if (current === 4) {
      magnX = 760; magnY = 155;
    } else if (current === 5) {
      // La lupa verifica correspondencia
      const bob = Math.sin(t / 200) * 3;
      magnX = 875; magnY = 160 + bob;
    } else if (current === 6) {
      magnX = 970; magnY = 150;
    }

    drawMagnifier(magnX, magnY, 3);
  }

  // Inicialización de eventos
  function init() {
    if ($('restart')) $('restart').addEventListener('click', () => { stop(); goTo(0); });
    if ($('previous')) $('previous').addEventListener('click', () => { stop(); goTo(current - 1); });
    if ($('next')) $('next').addEventListener('click', () => { stop(); goTo(current + 1); });
    if ($('play')) $('play').addEventListener('click', () => { if (playing) stop(); else start(); });

    document.querySelectorAll('.stations button').forEach(btn => {
      btn.addEventListener('click', () => {
        stop();
        const stageIdx = parseInt(btn.getAttribute('data-stage'), 10);
        goTo(stageIdx);
      });
    });

    // Atajos de teclado para accesibilidad
    window.addEventListener('keydown', (e) => {
      // Ignorar si el foco está en un input o textarea
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
      if (e.key === 'ArrowRight') {
        e.preventDefault();
        stop();
        goTo(current + 1);
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        stop();
        goTo(current - 1);
      } else if (e.key === ' ' || e.code === 'Space') {
        e.preventDefault();
        if (playing) stop(); else start();
      } else if (e.key === 'r' || e.key === 'R') {
        e.preventDefault();
        stop();
        goTo(0);
      }
    });

    reduced.addEventListener('change', () => {
      stop();
      updateView();
    });

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) stop();
    });

    updateView();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
