const API_BASE = "/api";

// 1. Verificar Token al cargar 
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    const path = window.location.pathname;

    // Si no hay token y no estás en el login, vuelve al inicio
    if (!token && path !== '/') {
        window.location.href = '/';
    }
    
    // Si estás en el dashboard, cargar los squads
    if (token && path.includes('dashboard')) {
        loadSquads();
    }
});

// 2. Cargar Squads
async function loadSquads(gameSlug = '') {
    const token = localStorage.getItem('access_token');
    const currentUser = localStorage.getItem('current_user'); // Para comparar dueño
    
    let url = `${API_BASE}/squads/`;
    if (gameSlug) url += `?game_slug=${gameSlug}`;

    try {
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const squads = await response.json();
        const container = document.getElementById('lista-squads');
        if (!container) return;
        
        container.innerHTML = '';

        squads.forEach(s => {
            // Comparación para mostrar botón eliminar
            const esMio = s.creator_username === currentUser;

            container.innerHTML += `
                <div class="col-12 animate__animated animate__fadeIn">
                    <div class="card-custom p-4 shadow-sm" style="border-left: 4px solid #0288DF">
                        <div class="d-flex justify-content-between mb-2">
                            <span class="text-indigo-400 fw-bold uppercase">${s.game_name || 'Juego'}</span>
                            <div class="d-flex gap-2">
                                <span class="badge bg-dark border border-secondary text-secondary">${s.rank_required}</span>
                                ${esMio ? `
                                    <button onclick="eliminarSquad(${s.id})" class="btn btn-sm btn-outline-danger border-0 p-0 px-1">
                                        <i class="fas fa-trash-alt"></i>
                                    </button>
                                ` : ''}
                            </div>
                        </div>
                        <p class="mb-3 text-white-50">${s.description}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="small text-white fw-bold"><i class="fas fa-user-circle me-1 text-warning"></i>${s.gamertag}</span>
                            <span class="small ${s.mic_required ? 'text-success' : 'text-danger'} fw-bold">
                                <i class="fas fa-microphone"></i> ${s.mic_required ? 'MIC ON' : 'MIC OFF'}
                            </span>
                        </div>
                    </div>
                </div>
            `;
        });
    } catch (error) {
        console.error("Error cargando squads:", error);
    }
}

// 3. Cerrar sesión
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('current_user');
    window.location.href = '/'; 
}