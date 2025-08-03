/**
 * Todo App - A-SDLC Example
 * Sistema de gerenciamento de tarefas com componente Kanban
 * Desenvolvido seguindo EXATAMENTE as especificações da story 20250803_123038_kanbam_kanbam.md
 */

// ===== CONFIGURAÇÕES DO APP =====
const APP_CONFIG = {
    STORAGE_KEY: 'todoAppData',
    MAX_TASK_LENGTH: 100,
    MAX_SUB_TASK_LENGTH: 80
};

// ===== TIPOS DE FILTRO =====
const FILTER_TYPES = {
    ALL: 'all',
    PENDING: 'pending',
    COMPLETED: 'completed'
};

// ===== MODOS DE VISUALIZAÇÃO =====
const VIEW_MODES = {
    LIST: 'list',
    KANBAN: 'kanban'
};

// ===== UTILITÁRIOS DE SEGURANÇA =====
class SecurityUtils {
    /**
     * Sanitiza HTML removendo tags e scripts perigosos
     * @param {string} text - Texto a ser sanitizado
     * @returns {string} - Texto sanitizado
     */
    static sanitizeHtml(text) {
        if (typeof text !== 'string') {
            return '';
        }

        // Remove todas as tags HTML
        const sanitized = text
            .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
            .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
            .replace(/<object\b[^<]*(?:(?!<\/object>)<[^<]*)*<\/object>/gi, '')
            .replace(/<embed\b[^<]*(?:(?!<\/embed>)<[^<]*)*<\/embed>/gi, '')
            .replace(/<[^>]*>/g, '')
            .replace(/javascript:/gi, '')
            .replace(/on\w+\s*=/gi, '')
            .trim();

        return sanitized;
    }

    /**
     * Escapa caracteres especiais para uso seguro em HTML
     * @param {string} text - Texto a ser escapado
     * @returns {string} - Texto escapado
     */
    static escapeHtml(text) {
        if (typeof text !== 'string') {
            return '';
        }

        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Valida e sanitiza entrada de texto
     * @param {string} text - Texto de entrada
     * @param {number} maxLength - Comprimento máximo permitido
     * @returns {string} - Texto validado e sanitizado
     */
    static validateAndSanitizeText(text, maxLength = 100) {
        if (!text || typeof text !== 'string') {
            return '';
        }

        const sanitized = this.sanitizeHtml(text.trim());
        
        if (sanitized.length > maxLength) {
            return sanitized.substring(0, maxLength);
        }

        return sanitized;
    }
}

// ===== ESTADO DA APLICAÇÃO =====
class TodoApp {
    constructor() {
        this.tasks = [];
        this.currentFilter = FILTER_TYPES.ALL;
        this.currentViewMode = VIEW_MODES.LIST;
        this.taskIdCounter = 1;
        
        this.initializeApp();
    }

    // ===== INICIALIZAÇÃO =====
    async initializeApp() {
        console.log('🚀 Inicializando Todo App - A-SDLC Example');
        
        this.loadTasksFromStorage();
        this.bindEventListeners();
        this.renderViewModeToggle();
        this.renderTasks();
        this.updateTaskCounter();
        
        console.log('✅ Todo App inicializada com sucesso');
    }

    // ===== ALTERNÂNCIA DE MODO DE VISUALIZAÇÃO =====
    toggleViewMode = () => {
        this.currentViewMode = this.currentViewMode === VIEW_MODES.LIST 
            ? VIEW_MODES.KANBAN 
            : VIEW_MODES.LIST;
        
        this.renderViewModeToggle();
        this.renderTasks();
        
        console.log(`🔄 Modo de visualização alterado para: ${this.currentViewMode}`);
        this.showToast('success', `Modo alterado para ${this.currentViewMode === VIEW_MODES.LIST ? 'Lista' : 'Kanban'}`);
    }

    renderViewModeToggle = () => {
        const toggleContainer = document.getElementById('viewModeToggle');
        if (!toggleContainer) return;

        const isListMode = this.currentViewMode === VIEW_MODES.LIST;
        
        toggleContainer.innerHTML = `
            <button class="view-mode-btn ${isListMode ? 'active' : ''}" onclick="todoApp.toggleViewMode()">
                <i class="fas fa-list"></i> Modo Lista
            </button>
            <button class="view-mode-btn ${!isListMode ? 'active' : ''}" onclick="todoApp.toggleViewMode()">
                <i class="fas fa-columns"></i> Modo Kanban
            </button>
        `;
    }

    // ===== GERENCIAMENTO DE EVENTOS =====
    bindEventListeners = () => {
        // Input de nova tarefa
        const taskInput = document.getElementById('taskInput');
        const addTaskBtn = document.getElementById('addTaskBtn');

        // Adicionar tarefa ao pressionar Enter
        taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.addTask();
            }
        });

        // Adicionar tarefa ao clicar no botão
        addTaskBtn.addEventListener('click', () => this.addTask());

        // Botões de filtro
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const filter = e.target.dataset.filter;
                this.setFilter(filter);
            });
        });

        // Botões de ação
        document.getElementById('clearCompletedBtn').addEventListener('click', () => this.clearCompletedTasks());
        document.getElementById('clearAllBtn').addEventListener('click', () => this.clearAllTasks());

        // Input de tarefa - validação em tempo real
        taskInput.addEventListener('input', (e) => {
            const addTaskBtn = document.getElementById('addTaskBtn');
            const taskText = SecurityUtils.validateAndSanitizeText(e.target.value, APP_CONFIG.MAX_TASK_LENGTH);
            addTaskBtn.disabled = taskText.length === 0;
        });
    }

    // ===== GERENCIAMENTO DE TAREFAS =====
    addTask = () => {
        const taskInput = document.getElementById('taskInput');
        const taskText = SecurityUtils.validateAndSanitizeText(taskInput.value, APP_CONFIG.MAX_TASK_LENGTH);

        // Validação
        if (!this.validateTaskInput(taskText)) {
            return;
        }

        try {
            const newTask = {
                id: this.generateTaskId(),
                text: taskText,
                completed: false,
                createdAt: new Date().toISOString()
            };

            this.tasks.push(newTask);
            this.taskIdCounter = this.generateTaskId();
            
            this.saveTasksToStorage();
            this.renderTasks();
            this.updateTaskCounter();
            
            taskInput.value = '';
            document.getElementById('addTaskBtn').disabled = true;
            
            console.log('✅ Nova tarefa adicionada:', newTask);
            this.showToast('success', 'Tarefa adicionada com sucesso!');
            
        } catch (error) {
            console.error('❌ Erro ao adicionar tarefa:', error);
            this.showToast('error', 'Erro ao adicionar tarefa');
        }
    }

    toggleTask = (taskId) => {
        try {
            const task = this.tasks.find(t => t.id === taskId);
            if (!task) return;

            task.completed = !task.completed;
            task.completedAt = task.completed ? new Date().toISOString() : null;
            
            this.saveTasksToStorage();
            this.renderTasks();
            this.updateTaskCounter();
            
            const message = task.completed ? 'Tarefa concluída!' : 'Tarefa marcada como pendente';
            console.log('✅ Tarefa atualizada:', task);
            this.showToast('success', message);
            
        } catch (error) {
            console.error('❌ Erro ao atualizar tarefa:', error);
            this.showToast('error', 'Erro ao atualizar tarefa');
        }
    }

    updateTaskStatus = (taskId, status) => {
        try {
            const task = this.tasks.find(t => t.id === taskId);
            
            if (!task) {
                throw new Error(`Tarefa com ID ${taskId} não encontrada`);
            }

            // Atualizar status
            task.status = status;
            
            // Se status for null, remover a propriedade
            if (status === null) {
                delete task.status;
            }
            
            // Salvar alterações
            this.saveTasksToStorage();
            
            // Atualizar interface
            this.renderTasks();
            this.updateTaskCounter();
            
            console.log('✅ Status da tarefa atualizado:', task);
            
        } catch (error) {
            console.error('❌ Erro ao atualizar status da tarefa:', error);
            this.showToast('error', 'Erro ao atualizar status da tarefa');
        }
    }

    deleteTask = (taskId) => {
        try {
            const taskIndex = this.tasks.findIndex(t => t.id === taskId);
            if (taskIndex === -1) return;

            const deletedTask = this.tasks.splice(taskIndex, 1)[0];
            
            this.saveTasksToStorage();
            this.renderTasks();
            this.updateTaskCounter();
            
            console.log('✅ Tarefa removida:', deletedTask);
            this.showToast('success', 'Tarefa removida!');
            
        } catch (error) {
            console.error('❌ Erro ao remover tarefa:', error);
            this.showToast('error', 'Erro ao remover tarefa');
        }
    }

    clearCompletedTasks = () => {
        try {
            const completedTasks = this.tasks.filter(task => task.completed);
            
            if (completedTasks.length === 0) {
                this.showToast('warning', 'Nenhuma tarefa concluída para remover');
                return;
            }

            this.tasks = this.tasks.filter(task => !task.completed);
            
            this.saveTasksToStorage();
            this.renderTasks();
            this.updateTaskCounter();
            
            console.log('✅ Tarefas concluídas removidas:', completedTasks.length);
            this.showToast('success', `${completedTasks.length} tarefa(s) concluída(s) removida(s)`);
            
        } catch (error) {
            console.error('❌ Erro ao limpar tarefas:', error);
            this.showToast('error', 'Erro ao limpar tarefas');
        }
    }

    clearAllTasks = () => {
        try {
            const totalTasks = this.tasks.length;
            
            if (totalTasks === 0) {
                this.showToast('warning', 'Nenhuma tarefa para remover');
                return;
            }

            this.tasks = [];
            this.taskIdCounter = 1;
            
            this.saveTasksToStorage();
            this.renderTasks();
            this.updateTaskCounter();
            
            console.log('✅ Todas as tarefas removidas');
            this.showToast('success', `Todas as ${totalTasks} tarefa(s) foram removidas`);
            
        } catch (error) {
            console.error('❌ Erro ao limpar tarefas:', error);
            this.showToast('error', 'Erro ao limpar tarefas');
        }
    }

    // ===== FILTROS =====
    setFilter = (filterType) => {
        this.currentFilter = filterType;
        
        // Atualizar botões de filtro
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.filter === filterType) {
                btn.classList.add('active');
            }
        });
        
        this.renderTasks();
        console.log('🔍 Filtro aplicado:', filterType);
    }

    getFilteredTasks = () => {
        switch (this.currentFilter) {
            case FILTER_TYPES.PENDING:
                return this.tasks.filter(task => !task.completed);
            case FILTER_TYPES.COMPLETED:
                return this.tasks.filter(task => task.completed);
            default:
                return this.tasks;
        }
    }

    // ===== RENDERIZAÇÃO =====
    renderTasks = () => {
        const todoList = document.getElementById('todoList');
        const emptyState = document.getElementById('emptyState');
        const kanbanSection = document.getElementById('kanbanSection');
        const todoListSection = document.querySelector('.todo-list-section');
        const actionsSection = document.querySelector('.actions-section');
        
        const filteredTasks = this.getFilteredTasks();
        
        if (this.currentViewMode === VIEW_MODES.LIST) {
            // ===== MODO LISTA =====
            kanbanSection.style.display = 'none';
            todoListSection.style.display = 'block';
            actionsSection.style.display = 'flex';
            
            if (filteredTasks.length === 0) {
                todoList.innerHTML = '';
                emptyState.classList.remove('hidden');
            } else {
                todoList.innerHTML = '';
                emptyState.classList.add('hidden');
                
                filteredTasks.forEach(task => {
                    const taskElement = this.createTaskElement(task);
                    todoList.appendChild(taskElement);
                });
            }
        } else {
            // ===== MODO KANBAN =====
            kanbanSection.style.display = 'block';
            todoListSection.style.display = 'none';
            actionsSection.style.display = 'none';
        }
    }

    createTaskElement = (task) => {
        const li = document.createElement('li');
        li.className = `todo-item ${task.completed ? 'completed' : ''}`;
        li.setAttribute('data-task-id', task.id);

        const subTasks = this.getSubTasks(task.id);
        const completedSubTasks = subTasks.filter(st => st.completed).length;
        const totalSubTasks = subTasks.length;

        // Sanitizar texto da tarefa
        const sanitizedText = SecurityUtils.escapeHtml(task.text);

        li.innerHTML = `
            <div class="todo-main-content">
                <input type="checkbox" class="todo-checkbox" ${task.completed ? 'checked' : ''} 
                       onchange="todoApp.toggleTask(${task.id})">
                <span class="todo-text" title="${sanitizedText}">
                    ${sanitizedText}
                </span>
                <div class="todo-actions">
                    ${totalSubTasks > 0 ? `<span class="sub-task-count">${completedSubTasks}/${totalSubTasks}</span>` : ''}
                    <button class="todo-action-btn" onclick="todoApp.toggleSubTaskSection(${task.id})" title="Sub-tarefas">
                        <i class="fas fa-list"></i>
                    </button>
                    <button class="todo-action-btn" onclick="todoApp.deleteTask(${task.id})" title="Remover">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="sub-task-section" id="subTaskSection_${task.id}" style="display: none;">
                <div class="sub-task-container">
                    <div class="sub-task-list" id="subTaskList_${task.id}">
                        ${this.renderSubTasks(task.id)}
                    </div>
                    <div class="sub-task-add-form">
                        <div class="sub-task-input-group">
                            <input type="text" class="sub-task-input" 
                                   placeholder="Adicionar sub tarefa..." 
                                   data-parent-task-id="${task.id}"
                                   onkeypress="if(event.key === 'Enter') todoApp.addSubTask(${task.id})">
                            <button class="sub-task-add-btn" onclick="todoApp.addSubTask(${task.id})">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        return li;
    }

    updateTaskCounter = () => {
        const taskCount = document.getElementById('taskCount');
        const totalTasks = this.tasks.length;
        const completedTasks = this.tasks.filter(task => task.completed).length;
        const pendingTasks = totalTasks - completedTasks;
        
        taskCount.textContent = `${totalTasks} tarefa${totalTasks !== 1 ? 's' : ''}`;
        
        // Atualizar botões de ação
        document.getElementById('clearCompletedBtn').disabled = completedTasks === 0;
        document.getElementById('clearAllBtn').disabled = totalTasks === 0;
    }

    // ===== STORAGE =====
    saveTasksToStorage = () => {
        try {
            const data = {
                tasks: this.tasks,
                taskIdCounter: this.taskIdCounter,
                currentFilter: this.currentFilter,
                currentViewMode: this.currentViewMode
            };
            
            localStorage.setItem(APP_CONFIG.STORAGE_KEY, JSON.stringify(data));
            console.log('💾 Dados salvos no localStorage');
            
        } catch (error) {
            console.error('❌ Erro ao salvar dados:', error);
            this.showToast('error', 'Erro ao salvar dados');
        }
    }

    loadTasksFromStorage = () => {
        try {
            const savedData = localStorage.getItem(APP_CONFIG.STORAGE_KEY);
            if (!savedData) return;

            const data = JSON.parse(savedData);
            
            this.tasks = data.tasks || [];
            this.taskIdCounter = data.taskIdCounter || 1;
            this.currentFilter = data.currentFilter || FILTER_TYPES.ALL;
            this.currentViewMode = data.currentViewMode || VIEW_MODES.LIST;
            
            console.log('📂 Dados carregados do localStorage:', this.tasks.length);
            
        } catch (error) {
            console.error('❌ Erro ao carregar dados salvos:', error);
            this.showToast('warning', 'Erro ao carregar dados salvos');
        }
    }

    // ===== TOAST =====
    showToast = (type, message) => {
        const toastContainer = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle'
        };
        
        // Sanitizar mensagem do toast
        const sanitizedMessage = SecurityUtils.escapeHtml(message);
        
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <i class="${icons[type]} toast-icon"></i>
            <span class="toast-message">${sanitizedMessage}</span>
        `;
        
        toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.parentNode.removeChild(toast);
            }, 300);
        }, 3000);
    }

    // ===== UTILITÁRIOS =====
    validateTaskInput = (text) => {
        if (!text || text.trim().length === 0) {
            this.showToast('warning', 'Digite uma tarefa antes de adicionar');
            return false;
        }

        if (text.length > APP_CONFIG.MAX_TASK_LENGTH) {
            this.showToast('warning', `Tarefa muito longa (máximo ${APP_CONFIG.MAX_TASK_LENGTH} caracteres)`);
            return false;
        }

        // Verificar duplicatas
        const isDuplicate = this.tasks.some(task => 
            task.text.toLowerCase().trim() === text.toLowerCase().trim()
        );

        if (isDuplicate) {
            this.showToast('warning', 'Esta tarefa já existe');
            return false;
        }

        return true;
    }

    generateTaskId = () => {
        return this.taskIdCounter++;
    }

    // ===== MÉTODOS DE SUB-TAREFAS =====
    getSubTasks = (parentTaskId) => {
        try {
            const allSubTasks = JSON.parse(localStorage.getItem('subTasks') || '{}');
            return allSubTasks[parentTaskId] || [];
        } catch (error) {
            console.error('❌ Erro ao carregar sub-tarefas:', error);
            return [];
        }
    }
    
    saveSubTasks = (parentTaskId, subTasks) => {
        try {
            const allSubTasks = JSON.parse(localStorage.getItem('subTasks') || '{}');
            allSubTasks[parentTaskId] = subTasks;
            localStorage.setItem('subTasks', JSON.stringify(allSubTasks));
        } catch (error) {
            console.error('❌ Erro ao salvar sub-tarefas:', error);
        }
    }
    
    addSubTask = (parentTaskId) => {
        const input = document.querySelector(`input[data-parent-task-id="${parentTaskId}"]`);
        if (!input) return;
        
        const title = SecurityUtils.validateAndSanitizeText(input.value, APP_CONFIG.MAX_SUB_TASK_LENGTH);
        if (!title) return;
        
        const subTasks = this.getSubTasks(parentTaskId);
        const newSubTask = {
            id: Date.now(),
            title: title,
            completed: false,
            createdAt: new Date().toISOString()
        };
        
        subTasks.push(newSubTask);
        this.saveSubTasks(parentTaskId, subTasks);
        
        input.value = '';
        this.renderTasks(); // Re-renderizar para atualizar contadores
        console.log('✅ Sub-tarefa adicionada:', newSubTask);
        this.showToast('success', 'Sub-tarefa adicionada!');
    }
    
    toggleSubTask = (parentTaskId, subTaskId) => {
        const subTasks = this.getSubTasks(parentTaskId);
        const subTask = subTasks.find(st => st.id === subTaskId);
        
        if (subTask) {
            subTask.completed = !subTask.completed;
            subTask.completedAt = subTask.completed ? new Date().toISOString() : null;
            this.saveSubTasks(parentTaskId, subTasks);
            this.renderTasks(); // Re-renderizar para atualizar contadores
        }
    }
    
    removeSubTask = (parentTaskId, subTaskId) => {
        const subTasks = this.getSubTasks(parentTaskId);
        const filteredSubTasks = subTasks.filter(st => st.id !== subTaskId);
        this.saveSubTasks(parentTaskId, filteredSubTasks);
        this.renderTasks(); // Re-renderizar para atualizar contadores
        console.log('✅ Sub-tarefa removida');
        this.showToast('success', 'Sub-tarefa removida!');
    }
    
    renderSubTasks = (parentTaskId) => {
        const subTasks = this.getSubTasks(parentTaskId);
        
        if (subTasks.length === 0) {
            return '<div class="sub-task-empty"><p>Nenhuma sub-tarefa</p></div>';
        }
        
        return subTasks.map(subTask => {
            const sanitizedTitle = SecurityUtils.escapeHtml(subTask.title);
            return `
                <div class="sub-task-item ${subTask.completed ? 'completed' : ''}" data-sub-task-id="${subTask.id}">
                    <input type="checkbox" class="sub-task-checkbox" ${subTask.completed ? 'checked' : ''} 
                           onchange="todoApp.toggleSubTask(${parentTaskId}, ${subTask.id})">
                    <span class="sub-task-title" title="${sanitizedTitle}">
                        ${sanitizedTitle}
                    </span>
                    <button class="sub-task-remove-btn" onclick="todoApp.removeSubTask(${parentTaskId}, ${subTask.id})">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
        }).join('');
    }
    
    toggleSubTaskSection = (taskId) => {
        const section = document.getElementById(`subTaskSection_${taskId}`);
        if (section) {
            const isHidden = section.style.display === 'none';
            section.style.display = isHidden ? 'block' : 'none';
        }
    }
}

// ===== INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔧 DOM carregado, inicializando aplicação...');
    
    const todoApp = new TodoApp();
    
    // Expor globalmente para uso pelo componente React
    window.todoApp = {
        addTask: todoApp.addTask.bind(todoApp),
        toggleTask: todoApp.toggleTask.bind(todoApp),
        updateTaskStatus: todoApp.updateTaskStatus.bind(todoApp),
        deleteTask: todoApp.deleteTask.bind(todoApp),
        clearCompletedTasks: todoApp.clearCompletedTasks.bind(todoApp),
        clearAllTasks: todoApp.clearAllTasks.bind(todoApp),
        setFilter: todoApp.setFilter.bind(todoApp),
        toggleViewMode: todoApp.toggleViewMode.bind(todoApp),
        toggleSubTaskSection: todoApp.toggleSubTaskSection.bind(todoApp),
        addSubTask: todoApp.addSubTask.bind(todoApp),
        toggleSubTask: todoApp.toggleSubTask.bind(todoApp),
        removeSubTask: todoApp.removeSubTask.bind(todoApp),
        // Expor propriedades para o componente React
        get tasks() { return todoApp.tasks; },
        get getFilteredTasks() { return todoApp.getFilteredTasks.bind(todoApp); }
    };
    
    console.log('✅ Todo App carregada com modos Lista e Kanban!');
    console.log('✅ [Debug] TodoApp global disponível:', !!window.todoApp);
});