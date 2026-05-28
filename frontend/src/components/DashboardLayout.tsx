import { NavLink } from 'react-router-dom'
import { useLocalStorage } from '../hooks/useLocalStorage'
import { useEffect } from 'react'
import type { ReactNode } from 'react'

const navItems = [
  { label: 'Dashboard', path: '/' },
  { label: 'Research', path: '/research' },
  { label: 'Documents', path: '/documents' },
  { label: 'Chat', path: '/chat' },
  { label: 'Settings', path: '/settings' },
]

function DashboardLayout({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useLocalStorage('theme', 'dark')

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark'
    setTheme(nextTheme)
  }

  return (
    <div className="flex min-h-screen">
      <aside className="w-72 border-r border-slate-200 bg-white p-6 text-slate-900 shadow-sm dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100">
        <div className="mb-8">
          <p className="text-xs uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Multi-Agent AI</p>
          <h1 className="mt-3 text-2xl font-semibold">Research Assistant</h1>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Explore, ingest documents, run agents, and chat with data.</p>
        </div>

        <nav className="space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `block rounded-2xl px-4 py-3 text-sm font-medium transition ${
                  isActive
                    ? 'bg-slate-900 text-white shadow-sm dark:bg-slate-700'
                    : 'text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <button
          type="button"
          onClick={toggleTheme}
          className="mt-8 inline-flex items-center justify-center rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100 dark:hover:bg-slate-800"
        >
          Toggle {theme === 'dark' ? 'Light' : 'Dark'} Mode
        </button>
      </aside>

      <main className="flex-1 p-6 lg:p-10">{children}</main>
    </div>
  )
}

export default DashboardLayout
