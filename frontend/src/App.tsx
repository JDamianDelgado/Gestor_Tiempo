import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "/api";
const TOKEN_KEY = import.meta.env.VITE_TOKEN_KEY;
const THEME_KEY = import.meta.env.VITE_THEME_KEY;

type Paciente = {
  nombre_ingreso: string;
  apellido: string;
  nro_habitacion: number;
  braden: number;
  riesgo: string;
};
type Actividad = { nombre: string };
type Categoria = { categoria: string; actividades: Actividad[] };
type Usuario = { id: number; nombre: string; apellido: string; email: string };

function ThemeToggle({
  darkMode,
  onToggle,
}: {
  darkMode: boolean;
  onToggle: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-label={darkMode ? "Activar modo claro" : "Activar modo oscuro"}
      className="rounded-lg border border-[#a77b83] bg-[#fffdf9] px-3 py-2 text-sm font-bold text-[#5b1f2a] shadow-sm transition hover:bg-white dark-toggle"
    >
      {darkMode ? "☼ Claro" : "☾ Oscuro"}
    </button>
  );
}

function getTokenSubject() {
  const token = localStorage.getItem(TOKEN_KEY);
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return Number(payload.sub);
  } catch {
    return null;
  }
}

async function apiRequest(path: string, options: RequestInit = {}) {
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  const data = await response.json().catch(() => ({}));
  if (!response.ok)
    throw new Error(data.detail || "No se pudo completar la solicitud.");
  return data;
}

function LoginForm({
  onLogin,
  darkMode,
  onToggleTheme,
}: {
  onLogin: () => void;
  darkMode: boolean;
  onToggleTheme: () => void;
}) {
  const [email, setEmail] = useState("");
  const [dni, setDni] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password: dni }),
      });
      localStorage.setItem(TOKEN_KEY, data.access_token);
      onLogin();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error de autenticación.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="panel-grid relative flex min-h-screen items-center justify-center p-5">
      <div className="absolute right-5 top-5">
        <ThemeToggle darkMode={darkMode} onToggle={onToggleTheme} />
      </div>
      <section className="login-panel fade-up grid w-full max-w-5xl overflow-hidden rounded-[20px] bg-[#5b1f2a] shadow-2xl md:grid-cols-[.85fr_1.15fr]">
        <div className="flex flex-col justify-between bg-[#f3eee5] p-8 md:p-12">
          <div>
            <p className="mb-12 text-sm font-bold uppercase tracking-[.22em] text-[#47715b]">
              ALCLA / cuidado conectado
            </p>
            <h1 className="max-w-sm text-5xl font-bold leading-[.96] tracking-[-.06em] text-[#5b1f2a] md:text-6xl">
              Tiempo que cuida.
            </h1>
            <p className="mt-6 max-w-xs text-[#4d6658]">
              Registra cada momento de atención con claridad y propósito.
            </p>
          </div>
          <div className="mt-16 flex items-end justify-between">
            <span className="text-7xl font-bold tracking-[-.1em] text-[#89a98f]">
              01
            </span>
            <span className="text-right text-xs uppercase tracking-widest text-[#527260]">
              Panel
              <br />
              asistencial
            </span>
          </div>
        </div>
        <form
          onSubmit={submit}
          className="flex flex-col justify-center p-8 text-white md:p-14"
        >
          <div className="mb-10">
            <p className="mb-3 text-sm font-medium uppercase tracking-[.2em] text-[#a6c9aa]">
              Acceso seguro
            </p>
            <h2 className="text-3xl font-semibold tracking-tight">
              Bienvenido de nuevo
            </h2>
            <p className="mt-2 text-sm text-[#abc0b2]">
              Ingresa tus credenciales para continuar.
            </p>
          </div>
          <label className="mb-5 block text-sm text-[#d5e5d7]">
            Email Gmail
            <input
              className="mt-2 w-full rounded-xl border border-[#a77b83] bg-[#713341] px-4 py-3.5 outline-none transition focus:border-[#f3eee5]"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="nombre@gmail.com"
              required
            />
          </label>
          <label className="mb-7 block text-sm text-[#d5e5d7]">
            CONTRASEÑA
            <input
              className="mt-2 w-full rounded-xl border border-[#a77b83] bg-[#713341] px-4 py-3.5 outline-none transition focus:border-[#f3eee5]"
              inputMode="numeric"
              value={dni}
              onChange={(e) => setDni(e.target.value)}
              placeholder="Tu contraseña"
              required
            />
          </label>
          {error && (
            <p className="mb-4 rounded-lg bg-[#8d493f] px-3 py-2 text-sm">
              {error}
            </p>
          )}
          <button
            disabled={loading}
            className="rounded-xl bg-[#f3eee5] px-5 py-3.5 font-bold text-[#5b1f2a] shadow-md transition hover:bg-white disabled:cursor-wait disabled:opacity-60"
          >
            {loading ? "Validando..." : "Entrar al panel  →"}
          </button>
          <p className="mt-5 text-center text-xs text-[#89a98f]">
            Tus datos están protegidos por autenticación JWT.
          </p>
        </form>
      </section>
    </main>
  );
}

function PacienteSelector({
  pacientes,
  selected,
  onSelect,
}: {
  pacientes: Paciente[];
  selected: Paciente | null;
  onSelect: (p: Paciente) => void;
}) {
  const [search, setSearch] = useState("");
  const filteredPacientes = pacientes.filter((paciente) => {
    const query = search.trim().toLowerCase();
    if (!query) return true;
    return `${paciente.nombre_ingreso} ${paciente.apellido} ${paciente.nro_habitacion}`
      .toLowerCase()
      .includes(query);
  });

  return (
    <section className="ui-card rounded-2xl border border-[#dfd4d0] bg-[#fffdf9] p-5 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-widest text-[#8a4654]">
            Paso 01
          </p>
          <h2 className="mt-1 text-xl font-semibold text-[#5b1f2a]">
            Selecciona un paciente
          </h2>
        </div>
        <span className="rounded-full bg-[#f2e9e4] px-3 py-1 text-xs font-bold text-[#7b3040]">
          {filteredPacientes.length} de {pacientes.length}
        </span>
      </div>
      <label className="mb-3 block text-sm font-semibold text-[#54232d]">
        Buscar paciente
        <input
          type="search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Nombre, apellido o habitación"
          className="mt-2 w-full rounded-xl border border-[#d9c8c9] bg-[#fbf9f5] px-4 py-3 text-[#54232d] outline-none transition placeholder:text-[#a18489] focus:border-[#8a4654]"
        />
      </label>
      <select
        className="w-full rounded-xl border border-[#d9c8c9] bg-[#fbf9f5] px-4 py-3 text-[#54232d] outline-none focus:border-[#8a4654]"
        value={
          selected
            ? `${selected.nombre_ingreso}-${selected.apellido}-${selected.nro_habitacion}`
            : ""
        }
        onChange={(event) => {
          const patient = filteredPacientes.find(
            (item) =>
              `${item.nombre_ingreso}-${item.apellido}-${item.nro_habitacion}` ===
              event.target.value,
          );
          if (patient) onSelect(patient);
        }}
        required
      >
        <option value="" disabled>
          {filteredPacientes.length
            ? "Elegir paciente..."
            : "No hay coincidencias"}
        </option>
        {filteredPacientes.map((p) => (
          <option
            key={`${p.nombre_ingreso}-${p.apellido}-${p.nro_habitacion}`}
            value={`${p.nombre_ingreso}-${p.apellido}-${p.nro_habitacion}`}
          >
            {p.nombre_ingreso} {p.apellido} · Hab. {p.nro_habitacion}
          </option>
        ))}
      </select>
      {selected && (
        <div className="mt-4 flex items-center justify-between rounded-xl bg-[#f2e9e4] px-4 py-3 text-sm">
          <span className="font-semibold text-[#632b38]">
            {selected.nombre_ingreso} {selected.apellido}
          </span>
          <span className="text-[#8a4654]">Riesgo {selected.riesgo}</span>
        </div>
      )}
    </section>
  );
}

function ActividadSelector({
  categorias,
  selected,
  onSelect,
}: {
  categorias: Categoria[];
  selected: Actividad | null;
  onSelect: (a: Actividad) => void;
}) {
  const [open, setOpen] = useState<string | null>(
    categorias[0]?.categoria || null,
  );
  return (
    <section className="ui-card rounded-2xl border border-[#dfd4d0] bg-[#f3eee5] p-5 shadow-sm">
      <div className="mb-4">
        <p className="text-xs font-bold uppercase tracking-widest text-[#8a4654]">
          Paso 02
        </p>
        <h2 className="mt-1 text-xl font-semibold text-[#5b1f2a]">
          Selecciona una actividad
        </h2>
      </div>
      <div className="divide-y divide-[#e8eee7]">
        {categorias.map((category) => (
          <div key={category.categoria} className="py-1">
            <button
              type="button"
              className="flex w-full items-center justify-between py-3 text-left font-semibold text-[#54232d]"
              onClick={() =>
                setOpen(open === category.categoria ? null : category.categoria)
              }
            >
              {category.categoria}
              <span className="text-xl font-normal text-[#a77b83]">
                {open === category.categoria ? "−" : "+"}
              </span>
            </button>
            {open === category.categoria && (
              <div className="mb-2 space-y-2">
                {category.actividades.map((activity) => (
                  <button
                    type="button"
                    key={activity.nombre}
                    onClick={() => onSelect(activity)}
                    className={`activity-option flex w-full items-center justify-between rounded-xl px-3 py-2.5 text-left text-sm transition ${selected?.nombre === activity.nombre ? "is-selected font-bold" : ""}`}
                  >
                    <span>{activity.nombre}</span>
                    <span>
                      {selected?.nombre === activity.nombre
                        ? "✓"
                        : "Seleccionar"}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

function GestorTiempoForm({
  paciente,
  actividad,
  usuario,
}: {
  paciente: Paciente;
  actividad: Actividad;
  usuario: Usuario;
}) {
  const [tiempo, setTiempo] = useState("30");
  const [grupal, setGrupal] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  async function submit(event: FormEvent) {
    event.preventDefault();
    setMessage("");
    setError("");
    setLoading(true);
    try {
      await apiRequest("/registros/", {
        method: "POST",
        body: JSON.stringify({
          paciente: `${paciente.nombre_ingreso} ${paciente.apellido}`,
          activity: actividad.nombre,
          usuario_id: usuario.id,
          usuario_nombre: `${usuario.nombre} ${usuario.apellido}`,
          tiempo: Number(tiempo),
          modo_grupal: grupal,
        }),
      });
      setMessage("Registro guardado correctamente.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo guardar.");
    } finally {
      setLoading(false);
    }
  }
  return (
    <section className="record-card rounded-2xl bg-[#5b1f2a] p-5 text-white shadow-lg md:p-6">
      <div className="mb-6 flex items-start justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-widest text-[#a6c9aa]">
            Paso 03
          </p>
          <h2 className="mt-1 text-xl font-semibold">Registrar tiempo</h2>
        </div>
        <span className="rounded-full bg-[#315846] px-3 py-1 text-xs text-[#c8ddc9]">
          Listo para guardar
        </span>
      </div>
      <div className="mb-6 grid gap-3 text-sm md:grid-cols-2">
        <div className="rounded-xl bg-[#244b3d] p-3">
          <span className="block text-xs text-[#91b49a]">Paciente</span>
          <strong>
            {paciente.nombre_ingreso} {paciente.apellido}
          </strong>
        </div>
        <div className="rounded-xl bg-[#244b3d] p-3">
          <span className="block text-xs text-[#91b49a]">Actividad</span>
          <strong>{actividad.nombre}</strong>
        </div>
        <div className="rounded-xl bg-[#244b3d] p-3 md:col-span-2">
          <span className="block text-xs text-[#91b49a]">Registrado por</span>
          <strong>
            {usuario.nombre} {usuario.apellido}
          </strong>
        </div>
      </div>
      <form onSubmit={submit} className="grid gap-4 md:grid-cols-2">
        <label className="text-sm text-[#d5e5d7]">
          Tiempo (minutos)
          <input
            className="mt-2 w-full rounded-xl border border-[#a77b83] bg-[#713341] px-4 py-3 text-white outline-none focus:border-[#f3eee5]"
            type="number"
            min="1"
            value={tiempo}
            onChange={(e) => setTiempo(e.target.value)}
            required
          />
        </label>
        <label className="flex cursor-pointer items-center gap-3 text-sm text-[#d5e5d7] md:col-span-2">
          <input
            type="checkbox"
            checked={grupal}
            onChange={(e) => setGrupal(e.target.checked)}
            className="h-5 w-5 accent-[#a6c9aa]"
          />{" "}
          Atención en modo grupal
        </label>
        <button
          disabled={loading}
          className="rounded-xl bg-[#f3eee5] px-5 py-3.5 font-bold text-[#5b1f2a] shadow-md transition hover:bg-white disabled:opacity-60 md:col-span-2"
        >
          {loading ? "Guardando..." : "Guardar registro  →"}
        </button>
      </form>
      {message && (
        <p className="mt-4 rounded-lg bg-[#315846] px-3 py-2 text-sm text-[#d9e6d5]">
          {message}
        </p>
      )}
      {error && (
        <p className="mt-4 rounded-lg bg-[#8d493f] px-3 py-2 text-sm">
          {error}
        </p>
      )}
    </section>
  );
}

function Dashboard({
  onLogout,
  darkMode,
  onToggleTheme,
}: {
  onLogout: () => void;
  darkMode: boolean;
  onToggleTheme: () => void;
}) {
  const [pacientes, setPacientes] = useState<Paciente[]>([]);
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [paciente, setPaciente] = useState<Paciente | null>(null);
  const [actividad, setActividad] = useState<Actividad | null>(null);
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [error, setError] = useState(() =>
    getTokenSubject() ? "" : "La sesión no contiene un usuario válido.",
  );
  const [loading, setLoading] = useState(() => Boolean(getTokenSubject()));
  useEffect(() => {
    const usuarioId = getTokenSubject();
    if (!usuarioId) return;
    Promise.all([
      apiRequest("/pacientes/lista"),
      apiRequest("/actividades/"),
      apiRequest(`/usuarios/${usuarioId}`),
    ])
      .then(([p, a, u]) => {
        setPacientes(p);
        setCategorias(a.categorias);
        setUsuario(u);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);
  return (
    <main className="panel-grid min-h-screen bg-[#f4f0e9] text-[#2e2327]">
      <header className="border-b border-[#dfd4d0] bg-[#fffdf9]/90 px-5 py-5 backdrop-blur md:px-10">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-[.25em] text-[#6e9076]">
              ALCLA / registro asistencial
            </p>
            <h1 className="mt-1 text-2xl font-bold tracking-tight text-[#193b31]">
              Gestor de tiempo
            </h1>
          </div>
          <div className="flex items-center gap-2">
            <ThemeToggle darkMode={darkMode} onToggle={onToggleTheme} />
            <button
              onClick={onLogout}
              className="rounded-lg bg-[#7b3040] px-4 py-2 text-xs font-bold uppercase tracking-wider text-white shadow-sm hover:bg-[#5b1f2a]"
            >
              Salir
            </button>
          </div>
        </div>
      </header>
      <div className="dashboard-content mx-auto max-w-6xl px-5 py-8 md:px-10 md:py-12">
        <div className="mb-8 max-w-xl">
          <p className="mb-2 text-sm font-semibold text-[#6e9076]">
            Turno activo · hoy
          </p>
          <h2 className="text-4xl font-bold leading-tight tracking-[-.05em] text-[#193b31] md:text-5xl">
            Cada registro cuenta.
          </h2>
          <p className="mt-3 text-[#67806c]">
            Selecciona a quién atendiste y describe el tiempo dedicado.
          </p>
        </div>
        {loading && (
          <div className="rounded-2xl bg-white p-8 text-center text-[#6e9076]">
            Cargando pacientes y actividades...
          </div>
        )}
        {error && (
          <div className="rounded-xl bg-[#f6dfd8] p-4 text-sm text-[#863f36]">
            {error}
          </div>
        )}
        {!loading && !error && (
          <div className="grid gap-5 lg:grid-cols-2">
            <PacienteSelector
              pacientes={pacientes}
              selected={paciente}
              onSelect={setPaciente}
            />
            <ActividadSelector
              categorias={categorias}
              selected={actividad}
              onSelect={setActividad}
            />
            {paciente && actividad && usuario && (
              <div className="lg:col-span-2">
                <GestorTiempoForm
                  paciente={paciente}
                  actividad={actividad}
                  usuario={usuario}
                />
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}

export default function App() {
  const [authenticated, setAuthenticated] = useState(
    Boolean(localStorage.getItem(TOKEN_KEY)),
  );
  const [darkMode, setDarkMode] = useState(
    () => localStorage.getItem(THEME_KEY) === "true",
  );
  useEffect(() => {
    document.documentElement.classList.toggle("dark-mode", darkMode);
    localStorage.setItem(THEME_KEY, String(darkMode));
  }, [darkMode]);
  const toggleTheme = () => setDarkMode((current) => !current);
  return authenticated ? (
    <Dashboard
      darkMode={darkMode}
      onToggleTheme={toggleTheme}
      onLogout={() => {
        localStorage.removeItem(TOKEN_KEY);
        setAuthenticated(false);
      }}
    />
  ) : (
    <LoginForm
      darkMode={darkMode}
      onToggleTheme={toggleTheme}
      onLogin={() => setAuthenticated(true)}
    />
  );
}
