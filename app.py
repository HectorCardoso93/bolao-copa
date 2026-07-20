from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import sqlite3, os
from fpdf import FPDF
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
app.secret_key = 'bolao-copa-2026-chave-secreta'

DB_PATH = os.path.join(os.path.dirname(__file__), 'bolao.db')
ADMIN_PASSWORD = 'copa2026'

BRASILIA = timezone(timedelta(hours=-3))

# ── MATCHES ──────────────────────────────────────────────────────────────────
MATCHES = [
    # FASE DE GRUPOS
    (1,  'group','A','México','África do Sul','11/06 16:00'),
    (2,  'group','A','Coreia do Sul','Tchéquia','11/06 23:00'),
    (25, 'group','A','Tchéquia','África do Sul','18/06 13:00'),
    (28, 'group','A','México','Coreia do Sul','18/06 22:00'),
    (53, 'group','A','Tchéquia','México','24/06 22:00'),
    (54, 'group','A','África do Sul','Coreia do Sul','24/06 22:00'),
    (3,  'group','B','Canadá','Bósnia-Herzegovina','12/06 16:00'),
    (8,  'group','B','Catar','Suíça','13/06 16:00'),
    (26, 'group','B','Suíça','Bósnia-Herzegovina','18/06 16:00'),
    (27, 'group','B','Canadá','Catar','18/06 19:00'),
    (51, 'group','B','Suíça','Canadá','24/06 16:00'),
    (52, 'group','B','Bósnia-Herzegovina','Catar','24/06 16:00'),
    (7,  'group','C','Brasil','Marrocos','13/06 19:00'),
    (5,  'group','C','Haiti','Escócia','13/06 22:00'),
    (30, 'group','C','Escócia','Marrocos','19/06 19:00'),
    (29, 'group','C','Brasil','Haiti','19/06 22:00'),
    (49, 'group','C','Escócia','Brasil','24/06 19:00'),
    (50, 'group','C','Marrocos','Haiti','24/06 19:00'),
    (4,  'group','D','Estados Unidos','Paraguai','12/06 22:00'),
    (6,  'group','D','Austrália','Turquia','13/06 01:00'),
    (31, 'group','D','Turquia','Paraguai','19/06 01:00'),
    (32, 'group','D','Estados Unidos','Austrália','19/06 16:00'),
    (59, 'group','D','Turquia','Estados Unidos','25/06 23:00'),
    (60, 'group','D','Paraguai','Austrália','25/06 23:00'),
    (10, 'group','E','Alemanha','Curaçao','14/06 14:00'),
    (9,  'group','E','Costa do Marfim','Equador','14/06 20:00'),
    (33, 'group','E','Alemanha','Costa do Marfim','20/06 17:00'),
    (34, 'group','E','Equador','Curaçao','20/06 21:00'),
    (55, 'group','E','Curaçao','Costa do Marfim','25/06 17:00'),
    (56, 'group','E','Equador','Alemanha','25/06 17:00'),
    (11, 'group','F','Holanda','Japão','14/06 17:00'),
    (12, 'group','F','Suécia','Tunísia','14/06 23:00'),
    (36, 'group','F','Tunísia','Japão','20/06 01:00'),
    (35, 'group','F','Holanda','Suécia','20/06 14:00'),
    (57, 'group','F','Japão','Suécia','25/06 20:00'),
    (58, 'group','F','Tunísia','Holanda','25/06 20:00'),
    (16, 'group','G','Bélgica','Egito','15/06 16:00'),
    (15, 'group','G','Irã','Nova Zelândia','15/06 22:00'),
    (39, 'group','G','Bélgica','Irã','21/06 16:00'),
    (40, 'group','G','Nova Zelândia','Egito','21/06 22:00'),
    (63, 'group','G','Egito','Irã','26/06 00:00'),
    (64, 'group','G','Nova Zelândia','Bélgica','26/06 00:00'),
    (14, 'group','H','Espanha','Cabo Verde','15/06 13:00'),
    (13, 'group','H','Arábia Saudita','Uruguai','15/06 19:00'),
    (38, 'group','H','Espanha','Arábia Saudita','21/06 13:00'),
    (37, 'group','H','Uruguai','Cabo Verde','21/06 19:00'),
    (65, 'group','H','Cabo Verde','Arábia Saudita','26/06 21:00'),
    (66, 'group','H','Uruguai','Espanha','26/06 21:00'),
    (17, 'group','I','França','Senegal','16/06 16:00'),
    (18, 'group','I','Iraque','Noruega','16/06 19:00'),
    (42, 'group','I','França','Iraque','22/06 18:00'),
    (41, 'group','I','Noruega','Senegal','22/06 21:00'),
    (61, 'group','I','Noruega','França','26/06 16:00'),
    (62, 'group','I','Senegal','Iraque','26/06 16:00'),
    (20, 'group','J','Áustria','Jordânia','16/06 01:00'),
    (19, 'group','J','Argentina','Argélia','16/06 22:00'),
    (44, 'group','J','Jordânia','Argélia','22/06 00:00'),
    (43, 'group','J','Argentina','Áustria','22/06 14:00'),
    (69, 'group','J','Argélia','Áustria','27/06 23:00'),
    (70, 'group','J','Jordânia','Argentina','27/06 23:00'),
    (23, 'group','K','Portugal','RD Congo','17/06 14:00'),
    (24, 'group','K','Uzbequistão','Colômbia','17/06 23:00'),
    (47, 'group','K','Portugal','Uzbequistão','23/06 14:00'),
    (48, 'group','K','Colômbia','RD Congo','23/06 23:00'),
    (71, 'group','K','Colômbia','Portugal','27/06 20:30'),
    (72, 'group','K','RD Congo','Uzbequistão','27/06 20:30'),
    (22, 'group','L','Inglaterra','Croácia','17/06 17:00'),
    (21, 'group','L','Gana','Panamá','17/06 20:00'),
    (45, 'group','L','Inglaterra','Gana','23/06 17:00'),
    (46, 'group','L','Panamá','Croácia','23/06 20:00'),
    (67, 'group','L','Panamá','Inglaterra','27/06 18:00'),
    (68, 'group','L','Croácia','Gana','27/06 18:00'),
    # SEGUNDA FASE
    (73,  'round_of_32', None,'2º Grupo A','2º Grupo B','28/06 16:00'),
    (74,  'round_of_32', None,'1º Grupo E','Melhor 3º','29/06 14:30'),
    (75,  'round_of_32', None,'1º Grupo F','2º Grupo C','29/06 22:00'),
    (76,  'round_of_32', None,'1º Grupo C','2º Grupo F','29/06 14:00'),
    (77,  'round_of_32', None,'1º Grupo I','Melhor 3º','30/06 18:00'),
    (78,  'round_of_32', None,'2º Grupo E','2º Grupo I','30/06 14:00'),
    (79,  'round_of_32', None,'1º Grupo A','Melhor 3º','30/06 22:00'),
    (80,  'round_of_32', None,'1º Grupo L','Melhor 3º','01/07 13:00'),
    (81,  'round_of_32', None,'1º Grupo D','Melhor 3º','01/07 21:00'),
    (82,  'round_of_32', None,'1º Grupo G','Melhor 3º','01/07 17:00'),
    (83,  'round_of_32', None,'2º Grupo K','2º Grupo L','02/07 20:00'),
    (84,  'round_of_32', None,'1º Grupo H','2º Grupo J','02/07 16:00'),
    (85,  'round_of_32', None,'1º Grupo B','Melhor 3º','02/07 00:00'),
    (86,  'round_of_32', None,'1º Grupo J','2º Grupo H','03/07 17:00'),
    (87,  'round_of_32', None,'1º Grupo K','Melhor 3º','03/07 22:30'),
    (88,  'round_of_32', None,'2º Grupo D','2º Grupo G','03/07 15:00'),
    # OITAVAS DE FINAL
    (89,  'round_of_16', None,'Vencedor J74','Vencedor J77','04/07 18:00'),
    (90,  'round_of_16', None,'Vencedor J73','Vencedor J75','04/07 14:00'),
    (91,  'round_of_16', None,'Vencedor J76','Vencedor J78','05/07 17:00'),
    (92,  'round_of_16', None,'Vencedor J79','Vencedor J80','05/07 21:00'),
    (93,  'round_of_16', None,'Vencedor J83','Vencedor J84','06/07 15:00'),
    (94,  'round_of_16', None,'Vencedor J81','Vencedor J82','06/07 20:00'),
    (95,  'round_of_16', None,'Vencedor J86','Vencedor J88','07/07 13:00'),
    (96,  'round_of_16', None,'Vencedor J85','Vencedor J87','07/07 17:00'),
    # QUARTAS DE FINAL
    (97,  'quarter_final', None,'Vencedor J89','Vencedor J90','09/07 17:00'),
    (98,  'quarter_final', None,'Vencedor J93','Vencedor J94','10/07 16:00'),
    (99,  'quarter_final', None,'Vencedor J91','Vencedor J92','11/07 18:00'),
    (100, 'quarter_final', None,'Vencedor J95','Vencedor J96','11/07 21:00'),
    # SEMIFINAL
    (101, 'semi_final', None,'Vencedor J97','Vencedor J98','14/07 16:00'),
    (102, 'semi_final', None,'Vencedor J99','Vencedor J100','15/07 16:00'),
    # 3º LUGAR / FINAL
    (103, 'third_place', None,'Perdedor SF1','Perdedor SF2','18/07 18:00'),
    (104, 'final',       None,'Vencedor SF1','Vencedor SF2','19/07 16:00'),
]

STAGE_LABELS = {
    'group':        'Fase de Grupos',
    'round_of_32':  'Segunda Fase',
    'round_of_16':  'Oitavas de Final',
    'quarter_final':'Quartas de Final',
    'semi_final':   'Semifinal',
    'third_place':  '3º Lugar',
    'final':        'Final',
}

DEADLINE_PHASES = [
    ('group',        'Fase de Grupos',     '2026-06-10T19:00'),
    ('round_of_32',  'Segunda Fase',        '2026-06-28T12:00'),
    ('round_of_16',  'Oitavas de Final',    '2026-07-04T12:00'),
    ('quarter_final','Quartas de Final',    '2026-07-09T12:00'),
    ('semi_final',   'Semifinal',            '2026-07-14T12:00'),
    ('final',        'Final / 3º Lugar',    '2026-07-19T12:00'),
]

GROUP_STAGES    = {'group'}
KNOCKOUT_STAGES = {'round_of_32','round_of_16','quarter_final','semi_final','third_place','final'}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE COLLATE NOCASE,
            email TEXT UNIQUE COLLATE NOCASE,
            pin TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_number INTEGER NOT NULL UNIQUE,
            stage TEXT NOT NULL,
            group_name TEXT,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            match_date TEXT NOT NULL,
            home_score INTEGER,
            away_score INTEGER,
            is_finished INTEGER DEFAULT 0,
            extra_time INTEGER DEFAULT 0,
            et_winner TEXT,
            et_home_score INTEGER,
            et_away_score INTEGER
        );
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            match_id INTEGER NOT NULL,
            home_score INTEGER NOT NULL,
            away_score INTEGER NOT NULL,
            pred_et_home INTEGER,
            pred_et_away INTEGER,
            pts_90 INTEGER DEFAULT 0,
            pts_et INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (match_id) REFERENCES matches(id),
            UNIQUE(user_id, match_id)
        );
        CREATE TABLE IF NOT EXISTS deadlines (
            stage TEXT PRIMARY KEY,
            deadline_dt TEXT NOT NULL
        );
    ''')
    conn.commit()
    # safe column migrations
    for tbl, col, defn in [
        ('users',       'pin',           'TEXT'),
        ('users',       'email',         'TEXT'),
        ('matches',     'extra_time',    'INTEGER DEFAULT 0'),
        ('matches',     'et_winner',     'TEXT'),
        ('matches',     'et_home_score', 'INTEGER'),
        ('matches',     'et_away_score', 'INTEGER'),
        ('predictions', 'pred_et_home',  'INTEGER'),
        ('predictions', 'pred_et_away',  'INTEGER'),
        ('predictions', 'pts_90',        'INTEGER DEFAULT 0'),
        ('predictions', 'pts_et',        'INTEGER DEFAULT 0'),
    ]:
        try:
            conn.execute(f'ALTER TABLE {tbl} ADD COLUMN {col} {defn}')
            conn.commit()
        except Exception:
            pass
    # seed default deadlines
    if conn.execute('SELECT COUNT(*) FROM deadlines').fetchone()[0] == 0:
        for stage, _, default_dt in DEADLINE_PHASES:
            conn.execute('INSERT OR IGNORE INTO deadlines (stage, deadline_dt) VALUES (?,?)',
                         (stage, default_dt))
        conn.commit()
    # seed matches (migration-safe)
    existing = {r[0] for r in conn.execute('SELECT match_number FROM matches').fetchall()}
    added = 0
    for m in MATCHES:
        if m[0] not in existing:
            conn.execute(
                'INSERT INTO matches (match_number,stage,group_name,home_team,away_team,match_date) VALUES(?,?,?,?,?,?)',
                (m[0], m[1], m[2], m[3], m[4], m[5])
            )
            added += 1
    if added:
        conn.commit()
    conn.close()

# ── DEADLINE HELPERS ──────────────────────────────────────────────────────────

def get_deadlines():
    conn = get_db()
    rows = conn.execute('SELECT stage, deadline_dt FROM deadlines').fetchall()
    conn.close()
    return {r['stage']: r['deadline_dt'] for r in rows}

def parse_deadline_dt(dt_str):
    try:
        return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M').replace(tzinfo=BRASILIA)
    except Exception:
        return None

def is_stage_closed(stage, deadlines):
    key = 'final' if stage == 'third_place' else stage
    dt_str = deadlines.get(key)
    if not dt_str:
        return False
    dt = parse_deadline_dt(dt_str)
    return dt is not None and datetime.now(BRASILIA) >= dt

def group_deadline_info(deadlines):
    dt_str = deadlines.get('group')
    if not dt_str:
        return {'closed': False, 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'deadline_iso': ''}
    dt = parse_deadline_dt(dt_str)
    if dt is None:
        return {'closed': False, 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'deadline_iso': ''}
    now       = datetime.now(BRASILIA)
    remaining = dt - now
    if remaining.total_seconds() <= 0:
        return {'closed': True, 'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'deadline_iso': dt.isoformat()}
    total_secs = int(remaining.total_seconds())
    return {
        'closed': False,
        'days':    total_secs // 86400,
        'hours':   (total_secs % 86400) // 3600,
        'minutes': (total_secs % 3600)  // 60,
        'seconds': total_secs % 60,
        'deadline_iso': dt.isoformat(),
    }

def fmt_deadline(dt_str):
    dt = parse_deadline_dt(dt_str)
    return dt.strftime('%d/%m/%Y %H:%M') if dt else '—'

# ── POINTS ────────────────────────────────────────────────────────────────────

def result_winner(h, a, et_winner=None):
    """Returns 'H', 'A', or 'D' (only possible in group stage)."""
    if h > a: return 'H'
    if a > h: return 'A'
    if et_winner: return et_winner
    return 'D'

def calc_pts_90(ph, pa, rh, ra, stage='group'):
    """Points for the 90-minute prediction.
    Group:    exact=5, result=2, wrong=0
    Knockout: exact=5, result=3, wrong=0
    """
    if ph == rh and pa == ra:
        return 5
    if result_winner(ph, pa) == result_winner(rh, ra):
        return 2 if stage == 'group' else 3
    return 0

def calc_pts_et(ph, pa, eth, eta):
    """Compare the user's prediction against the actual ET score.
    exact = 2 pts, result correct (not exact) = 1 pt, wrong = 0.
    Returns 0 if ET scores are None.
    """
    if eth is None or eta is None:
        return 0
    if ph == eth and pa == eta:
        return 2
    if result_winner(ph, pa) == result_winner(eth, eta):
        return 1
    return 0

def calc_points(ph, pa, rh, ra, stage='group', extra_time=False,
                et_home=None, et_away=None, et_winner=None,
                pred_et_home=None, pred_et_away=None):
    """Total = pts_90 + pts_et (additive, independent bets)."""
    pts = calc_pts_90(ph, pa, rh, ra, stage)
    if stage != 'group' and extra_time:
        pts += calc_pts_et(pred_et_home, pred_et_away, et_home, et_away)
    return pts

def recalc_all_points():
    conn = get_db()
    # Zera todos os pontos antes de recalcular (evita acúmulo de testes)
    conn.execute('UPDATE predictions SET pts_90=0, pts_et=0, points=0')
    for m in conn.execute(
        'SELECT id, stage, home_score, away_score, extra_time, et_home_score, et_away_score '
        'FROM matches WHERE is_finished=1'
    ).fetchall():
        for p in conn.execute(
            'SELECT id, home_score, away_score FROM predictions WHERE match_id=?', (m['id'],)
        ).fetchall():
            p90 = calc_pts_90(p['home_score'], p['away_score'],
                              m['home_score'], m['away_score'], m['stage'])
            pet = 0
            if m['stage'] != 'group' and m['extra_time']:
                pet = calc_pts_et(p['home_score'], p['away_score'],
                                  m['et_home_score'], m['et_away_score'])
            conn.execute(
                'UPDATE predictions SET pts_90=?, pts_et=?, points=? WHERE id=?',
                (p90, pet, p90 + pet, p['id'])
            )
    conn.commit()
    conn.close()

def build_groups(matches_raw, existing=None):
    groups = {}
    for m in matches_raw:
        key   = f"{m['group_name'] or ''}__{m['stage']}"
        label = f"Grupo {m['group_name']}" if m['group_name'] else STAGE_LABELS.get(m['stage'], m['stage'])
        if key not in groups:
            groups[key] = {'label': label, 'stage': m['stage'], 'matches': []}
        groups[key]['matches'].append({
            'match': m,
            'pred':  existing.get(m['id']) if existing else None
        })
    return groups

# ─── PÚBLICAS ────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    conn = get_db()
    total_players  = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    total_finished = conn.execute('SELECT COUNT(*) FROM matches WHERE is_finished=1').fetchone()[0]
    conn.close()
    deadlines = get_deadlines()
    dl = group_deadline_info(deadlines)
    return render_template('index.html', total_players=total_players,
                           total_finished=total_finished, deadline=dl)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    deadlines = get_deadlines()
    if is_stage_closed('group', deadlines):
        flash('O prazo para participar do bolão na fase de grupos encerrou.', 'erro')
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        pin      = request.form.get('pin', '').strip()
        if not username:
            flash('Nome de usuário obrigatório.', 'erro')
            return render_template('cadastro.html')
        if not email:
            flash('E-mail obrigatório.', 'erro')
            return render_template('cadastro.html')
        if not pin or not pin.isdigit() or len(pin) != 4:
            flash('A senha deve ter exatamente 4 dígitos numéricos.', 'erro')
            return render_template('cadastro.html')
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username,email,pin) VALUES(?,?,?)', (username, email, pin))
            conn.commit()
            user = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
            session['user_id'] = user['id']
            session['user']    = user['username']
            flash(f'Bem-vindo, {username}! Preencha seus palpites abaixo.', 'sucesso')
            return redirect(url_for('palpites'))
        except sqlite3.IntegrityError as e:
            if 'username' in str(e).lower():
                flash('Este nome de usuário já está em uso.', 'erro')
            else:
                flash('Este e-mail já está cadastrado.', 'erro')
        finally:
            conn.close()
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        pin   = request.form.get('pin', '').strip()
        if not email or not pin:
            flash('Informe e-mail e senha.', 'erro')
            return render_template('login.html')
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email=? COLLATE NOCASE', (email,)).fetchone()
        conn.close()
        if user and user['pin'] == pin:
            session['user_id'] = user['id']
            session['user']    = user['username']
            return redirect(url_for('palpites'))
        flash('E-mail ou senha incorretos.', 'erro')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/palpites', methods=['GET', 'POST'])
def palpites():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id   = session['user_id']
    deadlines = get_deadlines()
    conn = get_db()

    if request.method == 'POST':
        matches = conn.execute('SELECT id, match_number, stage FROM matches').fetchall()
        saved = 0
        for m in matches:
            if is_stage_closed(m['stage'], deadlines):
                continue
            h = request.form.get(f'home_{m["match_number"]}', '').strip()
            a = request.form.get(f'away_{m["match_number"]}', '').strip()
            if h != '' and a != '':
                try:
                    h, a = int(h), int(a)
                    if h < 0 or a < 0: continue
                    conn.execute('''
                        INSERT INTO predictions
                            (user_id,match_id,home_score,away_score,pts_90,pts_et,points)
                        VALUES(?,?,?,?,0,0,0)
                        ON CONFLICT(user_id,match_id) DO UPDATE
                        SET home_score=excluded.home_score, away_score=excluded.away_score
                    ''', (user_id, m['id'], h, a))
                    saved += 1
                except ValueError:
                    pass
        conn.commit()
        recalc_all_points()
        conn.close()
        flash(f'{saved} palpites salvos com sucesso!', 'sucesso')
        return redirect(url_for('palpites', confirmado=1))

    mode      = request.args.get('modo', '')
    confirmed = request.args.get('confirmado')
    matches_raw = conn.execute('SELECT * FROM matches ORDER BY match_number').fetchall()
    existing = {r['match_id']: r for r in conn.execute(
        'SELECT * FROM predictions WHERE user_id=?', (user_id,)
    ).fetchall()}
    total_pts = sum(r['points'] for r in existing.values())
    conn.close()

    has_predictions = len(existing) > 0
    if confirmed:
        mode = 'confirmado'
    elif has_predictions and mode != 'editar':
        mode = 'view'

    groups        = build_groups(matches_raw, existing)
    dl            = group_deadline_info(deadlines)
    groups_closed = is_stage_closed('group', deadlines)
    stages_closed = {stage: is_stage_closed(stage, deadlines) for stage in STAGE_LABELS}

    return render_template('palpites.html',
        groups=groups, mode=mode,
        has_predictions=has_predictions,
        total_pts=total_pts,
        total_palpites=len(existing),
        user=session['user'],
        deadline=dl,
        groups_closed=groups_closed,
        stages_closed=stages_closed,
    )

@app.route('/palpites/pdf')
def palpites_pdf():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id  = session['user_id']
    username = session['user']
    conn = get_db()
    # Only this user's predictions
    rows = conn.execute('''
        SELECT m.match_number, m.stage, m.group_name, m.home_team, m.away_team,
               m.match_date, m.home_score AS real_h, m.away_score AS real_a,
               m.is_finished, m.extra_time, m.et_winner,
               p.home_score AS pred_h, p.away_score AS pred_a, p.points
        FROM predictions p
        JOIN matches m ON m.id = p.match_id
        WHERE p.user_id = ?
        ORDER BY m.match_number
    ''', (user_id,)).fetchall()
    total_pts = conn.execute(
        'SELECT COALESCE(SUM(points),0) FROM predictions WHERE user_id=?', (user_id,)
    ).fetchone()[0]
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(12, 12, 12)

    pdf.set_fill_color(10, 22, 40)
    pdf.rect(0, 0, 210, 42, 'F')
    pdf.set_text_color(245, 197, 24)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_y(10)
    pdf.cell(0, 10, 'BOLAO COPA DO MUNDO 2026', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 7, f'Palpites de: {username}', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(245, 197, 24)
    pdf.cell(0, 7, f'Total de pontos: {total_pts}', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_y(50)

    W_NUM=10; W_HOME=64; W_SCORE=22; W_AWAY=64; W_DATE=16; W_PTS=10

    current_group = None
    for r in rows:
        grp       = r['group_name'] or STAGE_LABELS.get(r['stage'], r['stage'])
        grp_label = f"Grupo {grp}" if r['group_name'] else grp
        if grp_label != current_group:
            current_group = grp_label
            if pdf.get_y() > 260:
                pdf.add_page(); pdf.set_y(20)
            pdf.set_fill_color(10, 22, 40); pdf.set_text_color(245, 197, 24)
            pdf.set_font('Helvetica', 'B', 9)
            pdf.cell(0, 7, grp_label.upper(), fill=True, align='C', new_x='LMARGIN', new_y='NEXT')
        if pdf.get_y() > 268:
            pdf.add_page(); pdf.set_y(20)

        pred_h = r['pred_h'] if r['pred_h'] is not None else '-'
        pred_a = r['pred_a'] if r['pred_a'] is not None else '-'
        placar = f"{pred_h} x {pred_a}"

        pts_label = ''; pts_color = (120,120,120)
        if r['is_finished']:
            pts_label = f"{r['points']}pt"
            pts_color = (39,174,96) if r['points']==5 else \
                        ((200,160,0) if r['points'] in (2,3) else \
                        ((100,150,200) if r['points']==1 else (180,50,50)))

        even = (r['match_number'] % 2 == 0)
        pdf.set_fill_color(243 if even else 255, 245 if even else 255, 248 if even else 255)
        ROW_H = 6

        pdf.set_font('Helvetica','',7); pdf.set_text_color(140,140,140)
        pdf.cell(W_NUM,ROW_H,f"#{r['match_number']}",fill=True,align='R')
        pdf.set_font('Helvetica','B',8); pdf.set_text_color(30,30,30)
        pdf.cell(W_HOME,ROW_H,r['home_team'][:20],fill=True,align='R')
        pdf.set_font('Helvetica','B',9); pdf.set_text_color(10,80,180)
        pdf.cell(W_SCORE,ROW_H,placar,fill=True,align='C')
        pdf.set_font('Helvetica','B',8); pdf.set_text_color(30,30,30)
        pdf.cell(W_AWAY,ROW_H,r['away_team'][:20],fill=True,align='L')
        pdf.set_font('Helvetica','',7); pdf.set_text_color(120,120,120)
        pdf.cell(W_DATE,ROW_H,r['match_date'],fill=True,align='C')
        if pts_label:
            pdf.set_text_color(*pts_color); pdf.set_font('Helvetica','B',7)
        pdf.cell(W_PTS,ROW_H,pts_label,fill=True,align='C',new_x='LMARGIN',new_y='NEXT')

    pdf.set_y(-22)
    pdf.set_font('Helvetica','I',7); pdf.set_text_color(160,160,160)
    pdf.cell(0,5,'Grupos: 5=exato / 2=resultado  |  Mata-Mata 90min: 5=exato / 3=resultado  |  Prorrogacao: 2=exato / 1=resultado',align='C')

    response = make_response(bytes(pdf.output()))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=palpites-{username}.pdf'
    return response

@app.route('/classificacao')
def classificacao():
    conn = get_db()
    # ── Classificação Fase de Grupos ──
    players_group = conn.execute('''
        SELECT u.id, u.username,
               COUNT(p.id)                                            AS total_palpites,
               COALESCE(SUM(p.points),0)                             AS total_pontos,
               SUM(CASE WHEN p.points=5  THEN 1 ELSE 0 END)         AS acertos_exatos,
               SUM(CASE WHEN p.points=2  THEN 1 ELSE 0 END)         AS acertos_resultado,
               COALESCE(SUM(
                   CASE WHEN p.points=5 AND m.match_number IN (7,29,49)
                   THEN 1 ELSE 0 END
               ),0)                                                   AS acertos_brasil
        FROM users u
        LEFT JOIN predictions p ON p.user_id = u.id
        LEFT JOIN matches m ON m.id = p.match_id AND m.stage = 'group'
        WHERE p.id IS NULL OR m.stage = 'group'
        GROUP BY u.id
        ORDER BY total_pontos DESC, acertos_exatos DESC, acertos_brasil DESC, u.username ASC
    ''').fetchall()

    # ── Classificação Mata-Mata ──
    players_mm = conn.execute('''
        SELECT u.id, u.username,
               COUNT(p.id)                                            AS total_palpites,
               COALESCE(SUM(p.points),0)                             AS total_pontos,
               SUM(CASE WHEN p.pts_90=5  THEN 1 ELSE 0 END)         AS acertos_exatos,
               SUM(CASE WHEN p.pts_90=3  THEN 1 ELSE 0 END)         AS acertos_resultado,
               SUM(CASE WHEN p.pts_et=2  THEN 1 ELSE 0 END)         AS acertos_et_exatos,
               SUM(CASE WHEN p.pts_et=1  THEN 1 ELSE 0 END)         AS acertos_et_resultado
        FROM users u
        LEFT JOIN predictions p ON p.user_id = u.id
        LEFT JOIN matches m ON m.id = p.match_id AND m.stage != 'group'
        WHERE p.id IS NULL OR m.stage != 'group'
        GROUP BY u.id
        ORDER BY total_pontos DESC, acertos_exatos DESC, u.username ASC
    ''').fetchall()

    total_finished_group = conn.execute(
        "SELECT COUNT(*) FROM matches WHERE is_finished=1 AND stage='group'"
    ).fetchone()[0]
    total_finished_mm = conn.execute(
        "SELECT COUNT(*) FROM matches WHERE is_finished=1 AND stage!='group'"
    ).fetchone()[0]
    conn.close()

    return render_template('classificacao.html',
        players_group=players_group,
        players_mm=players_mm,
        total_finished_group=total_finished_group,
        total_finished_mm=total_finished_mm,
        total_players=len(players_group),
    )

# ─── ADMIN ────────────────────────────────────────────────────────────────────

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin'): return redirect(url_for('admin_jogos'))
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_jogos'))
        flash('Senha incorreta.', 'erro')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/jogos', methods=['GET', 'POST'])
def admin_jogos():
    if not session.get('admin'): return redirect(url_for('admin_login'))
    conn = get_db()
    if request.method == 'POST':
        for mid in request.form.getlist('match_ids'):
            h        = request.form.get(f'home_{mid}', '').strip()
            a        = request.form.get(f'away_{mid}', '').strip()
            finished = request.form.get(f'finished_{mid}') == '1'
            if h != '' and a != '':
                try:
                    conn.execute('UPDATE matches SET home_score=?,away_score=?,is_finished=? WHERE id=?',
                                 (int(h), int(a), 1 if finished else 0, int(mid)))
                except ValueError:
                    pass
            elif not finished:
                conn.execute('UPDATE matches SET home_score=NULL,away_score=NULL,is_finished=0 WHERE id=?', (int(mid),))
        conn.commit()
        recalc_all_points()
        flash('Resultados salvos! Pontuações recalculadas.', 'sucesso')
        conn.close()
        return redirect(url_for('admin_jogos'))
    matches = conn.execute("SELECT * FROM matches WHERE stage='group' ORDER BY match_number").fetchall()
    conn.close()
    groups = build_groups(matches)
    return render_template('admin_jogos.html', groups=groups)

@app.route('/admin/matamata', methods=['GET', 'POST'])
def admin_matamata():
    if not session.get('admin'): return redirect(url_for('admin_login'))
    conn = get_db()
    if request.method == 'POST':
        for mid in request.form.getlist('match_ids'):
            # Team names
            home_t = request.form.get(f'home_team_{mid}', '').strip()
            away_t = request.form.get(f'away_team_{mid}', '').strip()
            if home_t and away_t:
                conn.execute('UPDATE matches SET home_team=?, away_team=? WHERE id=?',
                             (home_t, away_t, int(mid)))
            # 90-min result
            finished_90 = request.form.get(f'finished_90_{mid}') == '1'
            h = request.form.get(f'home_{mid}', '').strip()
            a = request.form.get(f'away_{mid}', '').strip()
            if not finished_90:
                # Game still in progress — clear everything
                conn.execute(
                    'UPDATE matches SET home_score=NULL,away_score=NULL,is_finished=0,'
                    'extra_time=0,et_home_score=NULL,et_away_score=NULL WHERE id=?',
                    (int(mid),)
                )
            elif h != '' and a != '':
                try:
                    conn.execute(
                        'UPDATE matches SET home_score=?,away_score=?,is_finished=1 WHERE id=?',
                        (int(h), int(a), int(mid))
                    )
                    # Prorrogação
                    has_et = request.form.get(f'has_et_{mid}') == '1'
                    eth = request.form.get(f'et_home_{mid}', '').strip()
                    eta = request.form.get(f'et_away_{mid}', '').strip()
                    if has_et and eth != '' and eta != '':
                        conn.execute(
                            'UPDATE matches SET extra_time=1,et_home_score=?,et_away_score=? WHERE id=?',
                            (int(eth), int(eta), int(mid))
                        )
                    else:
                        conn.execute(
                            'UPDATE matches SET extra_time=0,et_home_score=NULL,et_away_score=NULL WHERE id=?',
                            (int(mid),)
                        )
                except ValueError:
                    pass
        conn.commit()
        recalc_all_points()
        flash('Mata-mata atualizado! Pontuações recalculadas.', 'sucesso')
        conn.close()
        return redirect(url_for('admin_matamata'))
    matches = conn.execute("SELECT * FROM matches WHERE stage!='group' ORDER BY match_number").fetchall()
    conn.close()
    groups = build_groups(matches)
    return render_template('admin_matamata.html', groups=groups)

@app.route('/admin/prazos', methods=['GET', 'POST'])
def admin_prazos():
    if not session.get('admin'): return redirect(url_for('admin_login'))
    conn = get_db()
    if request.method == 'POST':
        for stage, _, _ in DEADLINE_PHASES:
            dt_val = request.form.get(f'dl_{stage}', '').strip()
            if dt_val:
                conn.execute('INSERT OR REPLACE INTO deadlines (stage, deadline_dt) VALUES (?,?)',
                             (stage, dt_val))
        conn.commit()
        conn.close()
        flash('Prazos atualizados com sucesso!', 'sucesso')
        return redirect(url_for('admin_prazos'))
    deadlines = {r['stage']: r['deadline_dt'] for r in
                 conn.execute('SELECT stage, deadline_dt FROM deadlines').fetchall()}
    conn.close()
    phases = []
    for stage, label, default in DEADLINE_PHASES:
        dt_str = deadlines.get(stage, default)
        dt_obj = parse_deadline_dt(dt_str)
        closed = (datetime.now(BRASILIA) >= dt_obj) if dt_obj else False
        phases.append({'stage': stage, 'label': label, 'dt_str': dt_str,
                       'dt_fmt': fmt_deadline(dt_str), 'closed': closed})
    return render_template('admin_prazos.html', phases=phases)

@app.route('/admin/jogadores')
def admin_jogadores():
    if not session.get('admin'): return redirect(url_for('admin_login'))
    conn = get_db()
    players = conn.execute('''
        SELECT u.id, u.username, u.email, u.created_at,
               COUNT(p.id) as total_palpites,
               COALESCE(SUM(p.points),0) as total_pontos
        FROM users u
        LEFT JOIN predictions p ON p.user_id=u.id
        GROUP BY u.id ORDER BY u.username ASC
    ''').fetchall()
    conn.close()
    return render_template('admin_jogadores.html', players=players)

@app.route('/admin/jogadores/remover/<int:user_id>', methods=['POST'])
def admin_remover_jogador(user_id):
    if not session.get('admin'): return redirect(url_for('admin_login'))
    conn = get_db()
    user = conn.execute('SELECT username FROM users WHERE id=?', (user_id,)).fetchone()
    if user:
        conn.execute('DELETE FROM predictions WHERE user_id=?', (user_id,))
        conn.execute('DELETE FROM users WHERE id=?', (user_id,))
        conn.commit()
        flash(f'Jogador "{user["username"]}" removido.', 'sucesso')
    conn.close()
    return redirect(url_for('admin_jogadores'))

@app.route('/admin/jogadores/zerar/<int:user_id>', methods=['POST'])
def admin_zerar_jogador(user_id):
    if not session.get('admin'): return redirect(url_for('admin_login'))
    conn = get_db()
    user = conn.execute('SELECT username FROM users WHERE id=?', (user_id,)).fetchone()
    if user:
        conn.execute('DELETE FROM predictions WHERE user_id=?', (user_id,))
        conn.commit()
        flash(f'Todos os palpites de "{user["username"]}" zerados.', 'sucesso')
    conn.close()
    return redirect(url_for('admin_jogadores'))

@app.route('/admin/jogadores/zerar-matamata/<int:user_id>', methods=['POST'])
def admin_zerar_matamata_jogador(user_id):
    if not session.get('admin'): return redirect(url_for('admin_login'))
    conn = get_db()
    user = conn.execute('SELECT username FROM users WHERE id=?', (user_id,)).fetchone()
    if user:
        conn.execute('''DELETE FROM predictions WHERE user_id=?
                        AND match_id IN (SELECT id FROM matches WHERE stage != 'group')''',
                     (user_id,))
        conn.commit()
        flash(f'Palpites do mata-mata de "{user["username"]}" zerados.', 'sucesso')
    conn.close()
    return redirect(url_for('admin_jogadores'))

if __name__ == '__main__':
    init_db()
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 80))
    print(f'\n  Bolao Copa do Mundo 2026')
    print(f'  Acesse: http://localhost:{port}')
    print(f'  Na rede local: http://<seu-ip>:{port}\n')
    app.run(host=host, port=port, debug=False)
