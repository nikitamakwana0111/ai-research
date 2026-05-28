function DashboardPage() {
  return (
    <section className="space-y-6">
      <header className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-sky-500">Welcome back</p>
        <h2 className="mt-4 text-3xl font-semibold">Multi-Agent AI Research Assistant</h2>
        <p className="mt-2 max-w-2xl text-slate-600 dark:text-slate-300">
          Start a research pipeline, upload documents for RAG, or chat with your knowledge base using AI-powered agents.
        </p>
      </header>

      <div className="grid gap-6 xl:grid-cols-3">
        <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-xl font-semibold">Research Workflow</h3>
          <p className="mt-3 text-slate-600 dark:text-slate-300">Launch multi-agent research workflows that combine web search, analysis, summary, and report generation.</p>
        </article>

        <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-xl font-semibold">Document Intelligence</h3>
          <p className="mt-3 text-slate-600 dark:text-slate-300">Upload PDF research reports and query your documents with RAG-powered AI chat.</p>
        </article>

        <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-xl font-semibold">Modern Dashboard</h3>
          <p className="mt-3 text-slate-600 dark:text-slate-300">Control your workspace with an accessible interface and dark mode support.</p>
        </article>
      </div>
    </section>
  )
}

export default DashboardPage
