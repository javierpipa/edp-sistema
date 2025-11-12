# 📦 Instrucciones para configurar Git

## 1️⃣ Inicializar el repositorio Git

```bash
cd /home/javier/hd1/Codigo/JAVIER/edp
git init
```

## 2️⃣ Configurar usuario Git (si no lo has hecho antes)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

## 3️⃣ Agregar todos los archivos al staging

```bash
git add .
```

## 4️⃣ Verificar qué archivos se van a commitear

```bash
git status
```

Deberías ver todos los archivos del proyecto excepto los que están en `.gitignore` (como `venv/`, `.env`, `__pycache__/`, etc.)

## 5️⃣ Hacer el primer commit

```bash
git commit -m "Initial commit: Sistema EDP completo con dashboard, API REST y gestión de proyectos"
```

## 6️⃣ Crear repositorio en GitHub/GitLab (opcional)

### Opción A: GitHub
1. Ve a https://github.com/new
2. Crea un nuevo repositorio llamado `edp-sistema`
3. NO inicialices con README (ya tienes uno)

### Opción B: GitLab
1. Ve a https://gitlab.com/projects/new
2. Crea un nuevo proyecto llamado `edp-sistema`
3. NO inicialices con README

## 7️⃣ Conectar con el repositorio remoto

### Para GitHub:
```bash
git remote add origin https://github.com/TU_USUARIO/edp-sistema.git
git branch -M main
git push -u origin main
```

### Para GitLab:
```bash
git remote add origin https://gitlab.com/TU_USUARIO/edp-sistema.git
git branch -M main
git push -u origin main
```

## 8️⃣ Verificar el estado

```bash
git remote -v
git log --oneline
```

## 📋 Comandos útiles para el futuro

### Ver cambios
```bash
git status
git diff
```

### Agregar cambios
```bash
git add .                    # Agregar todos los archivos
git add archivo.py           # Agregar un archivo específico
```

### Hacer commit
```bash
git commit -m "Descripción del cambio"
```

### Subir cambios
```bash
git push
```

### Ver historial
```bash
git log
git log --oneline --graph
```

### Crear una rama
```bash
git checkout -b feature/nueva-funcionalidad
```

### Cambiar de rama
```bash
git checkout main
git checkout feature/nueva-funcionalidad
```

### Fusionar rama
```bash
git checkout main
git merge feature/nueva-funcionalidad
```

## 🔒 Archivos importantes que NO se suben (ya están en .gitignore)

- `venv/` - Entorno virtual
- `.env` - Variables de entorno (contraseñas, secrets)
- `__pycache__/` - Archivos compilados de Python
- `db.sqlite3` - Base de datos local
- `media/` - Archivos subidos por usuarios
- `*.log` - Archivos de log

## ✅ Archivos que SÍ se suben

- Todo el código fuente (`.py`, `.html`, `.js`, `.css`)
- `requirements.txt` - Dependencias del proyecto
- `.env.example` - Ejemplo de variables de entorno
- `README.md` - Documentación
- `manage.py` - Script de Django
- Templates y archivos estáticos

## 🎯 Buenas prácticas

1. **Commits frecuentes**: Haz commits pequeños y frecuentes
2. **Mensajes descriptivos**: Usa mensajes claros como:
   - `feat: Agregar filtro de actividades por estado`
   - `fix: Corregir cálculo de avance en cuadro de control`
   - `docs: Actualizar README con instrucciones de instalación`
3. **Branches**: Usa ramas para nuevas funcionalidades
4. **Pull antes de Push**: Siempre haz `git pull` antes de `git push`
5. **No subas secrets**: Nunca subas `.env` o archivos con contraseñas

## 🚨 Si cometiste un error

### Deshacer último commit (mantener cambios)
```bash
git reset --soft HEAD~1
```

### Deshacer cambios en un archivo
```bash
git checkout -- archivo.py
```

### Ver qué cambió en el último commit
```bash
git show
```

## 📝 Ejemplo de flujo de trabajo

```bash
# 1. Hacer cambios en el código
# 2. Ver qué cambió
git status
git diff

# 3. Agregar cambios
git add .

# 4. Hacer commit
git commit -m "feat: Agregar paginación en lista de actividades"

# 5. Subir a GitHub/GitLab
git push

# 6. Repetir
```

## 🎉 ¡Listo!

Tu proyecto ahora está bajo control de versiones y respaldado en la nube.
