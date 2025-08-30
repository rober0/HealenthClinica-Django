import { defineConfig } from 'vite';
import { resolve } from 'path';
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  base: "/static/",
   plugins: [
    tailwindcss(),
  ],
  build: {
    manifest: "manifest.json",
    outDir: resolve("./assets"),
    assetsDir: "django-assets",
    rollupOptions: {
      input: {
        global: resolve('./static/css/global.css'),
        simple_datatables: resolve('./static/js/datatables.js'),
        simple_datatables_css: resolve('./static/css/datatables.css'),
        intl_input: resolve('./static/js/intl.js'),
        agenda_adm: resolve('./static/js/agenda/agendaadm.js'),
        agenda_med: resolve('./static/js/agenda/agendamed.js'),
        agenda_pac: resolve('./static/js/agenda/agendapac.js')
      }
    }
  }
})