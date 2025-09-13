// Gerenciador de Lista de Tarefas
class TaskManager {
    constructor() {
        this.tasks = [];
        this.currentFilter = 'all';
        this.currentView = 'kanban';
        this.taskIdCounter = 1;
        this.taskToDelete = null;
        this.activeSubtaskInput = null;
        this.draggedTask = null;
        
        this.initializeElements();
        this.bindEvents();
        this.loadTasks();
        this.migrateExistingTasks();
        this.render();
    }

    // Inicializar elementos DOM
    initializeElements() {
        this.elements = {
            taskInput: document.getElementById('taskInput'),
            addTaskBtn: document.getElementById('addTaskBtn'),
            
            // Views
            kanbanView: document.getElementById('kanbanView'),
            listView: document.getElementById('listView'),
            kanbanBoard: document.getElementById('kanbanBoard'),
            listSection: document.getElementById('listSection'),
            listFilters: document.getElementById('listFilters'),
            
            // Kanban columns
            notStartedTasks: document.getElementById('notStartedTasks'),
            inProgressTasks: document.getElementById('inProgressTasks'),
            completedTasks: document.getElementById('completedTasks'),
            
            // List view
            tasksList: document.getElementById('tasksList'),
            emptyState: document.getElementById('emptyState'),
            filterBtns: document.querySelectorAll('.filter-btn'),
            
            // Counts
            notStartedCount: document.getElementById('notStartedCount'),
            inProgressCount: document.getElementById('inProgressCount'),
            allCount: document.getElementById('allCount'),
            pendingCount: document.getElementById('pendingCount'),
            completedCount: document.getElementById('completedCount'),
            
            // Controls
            clearCompleted: document.getElementById('clearCompleted'),
            confirmModal: document.getElementById('confirmModal'),
            cancelDelete: document.getElementById('cancelDelete'),
            confirmDelete: document.getElementById('confirmDelete')
        };
        

    }

    // Vincular eventos
    bindEvents() {
        // Adicionar tarefa
        this.elements.addTaskBtn.addEventListener('click', () => this.addTask());
        this.elements.taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addTask();
            }
        });

        // View toggle
        this.elements.kanbanView.addEventListener('click', () => {
            this.setView('kanban');
        });

        this.elements.listView.addEventListener('click', () => {
            this.setView('list');
        });

        // Filtros (apenas para list view)
        this.elements.filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setFilter(e.target.dataset.filter);
            });
        });

        // Limpar tarefas concluídas
        this.elements.clearCompleted.addEventListener('click', () => {
            this.clearCompletedTasks();
        });

        // Modal de confirmação
        this.elements.cancelDelete.addEventListener('click', () => {
            this.hideConfirmModal();
        });

        this.elements.confirmDelete.addEventListener('click', () => {
            this.confirmDeleteTask();
        });

        // Fechar modal clicando fora
        this.elements.confirmModal.addEventListener('click', (e) => {
            if (e.target === this.elements.confirmModal) {
                this.hideConfirmModal();
            }
        });

        // Navegação por teclado no modal
        document.addEventListener('keydown', (e) => {
            if (this.elements.confirmModal.classList.contains('show')) {
                if (e.key === 'Escape') {
                    this.hideConfirmModal();
                } else if (e.key === 'Enter') {
                    this.confirmDeleteTask();
                }
            }
        });
    }

    // Adicionar nova tarefa
    addTask() {
        const text = this.elements.taskInput.value.trim();
        
        if (!text) {
            this.showInputError('Por favor, digite uma tarefa válida');
            return;
        }

        if (text.length > 200) {
            this.showInputError('A tarefa não pode ter mais de 200 caracteres');
            return;
        }

        // Verificar se já existe uma tarefa idêntica
        if (this.tasks.some(task => task.text.toLowerCase() === text.toLowerCase())) {
            this.showInputError('Esta tarefa já existe na sua lista');
            return;
        }

        const task = {
            id: this.taskIdCounter++,
            text: text,
            status: 'not_started', // not_started, in_progress, completed
            completed: false,
            createdAt: new Date().toISOString(),
            completedAt: null,
            subtasks: [],
            parentId: null
        };

        this.tasks.unshift(task);
        this.elements.taskInput.value = '';
        this.saveTasks();
        this.render();
        
        // Feedback visual
        this.showSuccessMessage('Tarefa adicionada com sucesso!');
    }

    // Alternar estado de conclusão da tarefa
    toggleTask(id) {
        const task = this.findTaskById(id);
        if (task) {
            task.completed = !task.completed;
            task.completedAt = task.completed ? new Date().toISOString() : null;
            
            // Atualizar status baseado na conclusão
            if (task.completed) {
                task.status = 'completed';
            } else if (task.status === 'completed') {
                task.status = 'not_started';
            }
            
            // Se é uma tarefa principal, atualizar subtarefas
            if (task.subtasks && task.subtasks.length > 0) {
                task.subtasks.forEach(subtask => {
                    subtask.completed = task.completed;
                    subtask.completedAt = task.completed ? new Date().toISOString() : null;
                    subtask.status = task.completed ? 'completed' : 'not_started';
                });
            }
            
            // Se é uma subtarefa, verificar se deve marcar a tarefa pai
            if (task.parentId) {
                this.updateParentTaskStatus(task.parentId);
            }
            
            this.saveTasks();
            this.render();
            
            const message = task.completed ? 
                'Tarefa marcada como concluída! 🎉' : 
                'Tarefa desmarcada';
            this.showSuccessMessage(message);
        }
    }

    // Solicitar confirmação para deletar tarefa
    deleteTask(id) {
        this.taskToDelete = id;
        this.showConfirmModal();
    }

    // Confirmar exclusão da tarefa
    confirmDeleteTask() {
        if (this.taskToDelete) {
            this.deleteTaskAndSubtasks(this.taskToDelete);
            this.saveTasks();
            this.render();
            this.hideConfirmModal();
            this.showSuccessMessage('Tarefa excluída com sucesso');
            this.taskToDelete = null;
        }
    }

    // Deletar tarefa e suas subtarefas recursivamente
    deleteTaskAndSubtasks(taskId) {
        const task = this.findTaskById(taskId);
        if (task && task.subtasks) {
            // Deletar subtarefas primeiro
            task.subtasks.forEach(subtask => {
                this.deleteTaskAndSubtasks(subtask.id);
            });
        }
        
        // Deletar a tarefa principal
        this.tasks = this.tasks.filter(t => t.id !== taskId);
        
        // Remover das subtarefas de outras tarefas
        this.tasks.forEach(t => {
            if (t.subtasks) {
                t.subtasks = t.subtasks.filter(st => st.id !== taskId);
            }
        });
    }

    // Definir filtro
    setFilter(filter) {
        this.currentFilter = filter;
        
        // Atualizar botões de filtro
        this.elements.filterBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
        });
        
        this.render();
    }

    // Limpar tarefas concluídas
    clearCompletedTasks() {
        const completedCount = this.tasks.filter(t => t.status === 'completed').length;
        
        if (completedCount === 0) {
            this.showInputError('Não há tarefas finalizadas para limpar');
            return;
        }

        this.tasks = this.tasks.filter(t => t.status !== 'completed');
        this.saveTasks();
        this.render();
        this.showSuccessMessage(`${completedCount} tarefa(s) finalizada(s) removida(s)`);
    }

    // Obter tarefas filtradas
    getFilteredTasks() {
        // Garantir que todas as tarefas tenham status
        this.tasks.forEach(task => {
            if (!task.status) {
                task.status = task.completed ? 'completed' : 'not_started';
            }
        });
        
        switch (this.currentFilter) {
            case 'pending':
                return this.tasks.filter(t => t.status !== 'completed');
            case 'completed':
                return this.tasks.filter(t => t.status === 'completed');
            default:
                return this.tasks;
        }
    }

    // Encontrar tarefa por ID (incluindo subtarefas)
    findTaskById(id) {
        for (const task of this.tasks) {
            if (task.id === id) {
                return task;
            }
            if (task.subtasks) {
                for (const subtask of task.subtasks) {
                    if (subtask.id === id) {
                        return subtask;
                    }
                }
            }
        }
        return null;
    }

    // Adicionar subtarefa
    addSubtask(parentId, text) {
        const parentTask = this.findTaskById(parentId);
        if (!parentTask) return;

        if (!text.trim()) {
            this.showInputError('Por favor, digite uma subtarefa válida');
            return;
        }

        const subtask = {
            id: this.taskIdCounter++,
            text: text.trim(),
            status: 'not_started',
            completed: false,
            createdAt: new Date().toISOString(),
            completedAt: null,
            subtasks: [],
            parentId: parentId
        };

        if (!parentTask.subtasks) {
            parentTask.subtasks = [];
        }

        parentTask.subtasks.push(subtask);
        this.saveTasks();
        this.render();
        this.hideSubtaskInput();
        this.showSuccessMessage('Subtarefa adicionada com sucesso!');
    }

    // Atualizar status da tarefa pai baseado nas subtarefas
    updateParentTaskStatus(parentId) {
        const parentTask = this.findTaskById(parentId);
        if (!parentTask || !parentTask.subtasks || parentTask.subtasks.length === 0) {
            return;
        }

        const allSubtasksCompleted = parentTask.subtasks.every(st => st.status === 'completed');
        if (allSubtasksCompleted && parentTask.status !== 'completed') {
            parentTask.completed = true;
            parentTask.status = 'completed';
            parentTask.completedAt = new Date().toISOString();
        }
    }

    // Mostrar input de subtarefa
    showSubtaskInput(parentId) {
        this.hideSubtaskInput(); // Esconder outros inputs ativos
        
        const parentElement = document.querySelector(`[data-task-id="${parentId}"]`);
        if (!parentElement) return;

        const inputContainer = document.createElement('div');
        inputContainer.className = 'subtask-input-container';
        inputContainer.innerHTML = `
            <div class="subtask-input-group">
                <input type="text" 
                       class="subtask-input" 
                       placeholder="Digite sua subtarefa..." 
                       maxlength="150">
                <button class="subtask-add-btn" title="Adicionar subtarefa">✓</button>
                <button class="subtask-cancel-btn" title="Cancelar">✕</button>
            </div>
        `;

        const subtasksList = parentElement.querySelector('.subtasks-list');
        if (subtasksList) {
            subtasksList.appendChild(inputContainer);
        }

        const input = inputContainer.querySelector('.subtask-input');
        const addBtn = inputContainer.querySelector('.subtask-add-btn');
        const cancelBtn = inputContainer.querySelector('.subtask-cancel-btn');

        this.activeSubtaskInput = { parentId, inputContainer, input };

        // Eventos
        addBtn.addEventListener('click', () => {
            this.addSubtask(parentId, input.value);
        });

        cancelBtn.addEventListener('click', () => {
            this.hideSubtaskInput();
        });

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.addSubtask(parentId, input.value);
            } else if (e.key === 'Escape') {
                this.hideSubtaskInput();
            }
        });

        input.focus();
    }

    // Esconder input de subtarefa
    hideSubtaskInput() {
        if (this.activeSubtaskInput) {
            const { inputContainer } = this.activeSubtaskInput;
            if (inputContainer && inputContainer.parentNode) {
                inputContainer.parentNode.removeChild(inputContainer);
            }
            this.activeSubtaskInput = null;
        }
    }

    // Renderizar lista de tarefas
    render() {
        this.updateCounts();
        if (this.currentView === 'kanban') {
            this.renderKanban();
        } else {
            this.renderList();
        }
        this.updateEmptyState();
        this.updateClearButton();
    }

    // Alternar visualização
    setView(view) {
        this.currentView = view;
        
        // Atualizar botões
        this.elements.kanbanView.classList.toggle('active', view === 'kanban');
        this.elements.listView.classList.toggle('active', view === 'list');
        
        // Mostrar/esconder seções
        this.elements.kanbanBoard.style.display = view === 'kanban' ? 'block' : 'none';
        this.elements.listSection.style.display = view === 'list' ? 'block' : 'none';
        this.elements.listFilters.style.display = view === 'list' ? 'flex' : 'none';
        
        // Garantir que os botões de view sempre estejam visíveis
        this.elements.kanbanView.style.display = 'block';
        this.elements.listView.style.display = 'block';
        
        this.render();
    }

    // Atualizar contadores (incluindo subtarefas)
    updateCounts() {
        let allCount = 0;
        let pendingCount = 0;
        let completedCount = 0;
        let notStartedCount = 0;
        let inProgressCount = 0;

        const countTask = (task) => {
            allCount++;
            
            if (task.status === 'completed') {
                completedCount++;
            } else if (task.status === 'in_progress') {
                inProgressCount++;
                pendingCount++;
            } else {
                notStartedCount++;
                pendingCount++;
            }
            
            if (task.subtasks) {
                task.subtasks.forEach(countTask);
            }
        };

        this.tasks.forEach(countTask);

        // Atualizar contadores na interface
        if (this.elements.allCount) this.elements.allCount.textContent = allCount;
        if (this.elements.pendingCount) this.elements.pendingCount.textContent = pendingCount;
        if (this.elements.completedCount) this.elements.completedCount.textContent = completedCount;
        if (this.elements.notStartedCount) this.elements.notStartedCount.textContent = notStartedCount;
        if (this.elements.inProgressCount) this.elements.inProgressCount.textContent = inProgressCount;
    }

    // Renderizar Kanban
    renderKanban() {
        const tasksByStatus = {
            not_started: [],
            in_progress: [],
            completed: []
        };

        // Organizar tarefas por status
        this.tasks.forEach(task => {
            if (tasksByStatus[task.status]) {
                tasksByStatus[task.status].push(task);
            }
        });

        // Renderizar cada coluna
        this.renderKanbanColumn('notStartedTasks', tasksByStatus.not_started);
        this.renderKanbanColumn('inProgressTasks', tasksByStatus.in_progress);
        this.renderKanbanColumn('completedTasks', tasksByStatus.completed);
    }

    // Renderizar coluna do Kanban
    renderKanbanColumn(columnId, tasks) {
        const column = this.elements[columnId];
        if (!column) return;

        column.innerHTML = '';
        
        tasks.forEach(task => {
            const taskCard = this.createKanbanCard(task);
            column.appendChild(taskCard);
        });
    }

    // Renderizar lista (view tradicional)
    renderList() {
        const filteredTasks = this.getFilteredTasks();
        
        if (!this.elements.tasksList) {
            console.error('Elemento tasksList não encontrado!');
            return;
        }
        
        this.elements.tasksList.innerHTML = '';
        
        filteredTasks.forEach(task => {
            const taskElement = this.createTaskElement(task);
            this.elements.tasksList.appendChild(taskElement);
        });
    }

    // Criar elemento de tarefa
    createTaskElement(task, level = 0) {
        const li = document.createElement('li');
        li.className = `task-item ${task.completed ? 'completed' : ''} ${level > 0 ? 'subtask' : ''}`;
        li.setAttribute('role', 'listitem');
        li.setAttribute('data-task-id', task.id);
        li.style.marginLeft = level > 0 ? `${level * 30}px` : '0';
        
        const hasSubtasks = task.subtasks && task.subtasks.length > 0;
        const subtaskCount = hasSubtasks ? task.subtasks.length : 0;
        const completedSubtasks = hasSubtasks ? task.subtasks.filter(st => st.completed).length : 0;
        
        li.innerHTML = `
            <div class="task-main">
                <div class="task-checkbox ${task.completed ? 'checked' : ''}" 
                     onclick="taskManager.toggleTask(${task.id})"
                     role="checkbox" 
                     aria-checked="${task.completed}"
                     tabindex="0"
                     onkeypress="if(event.key==='Enter'||event.key===' ') taskManager.toggleTask(${task.id})">
                    ${task.completed ? '✓' : ''}
                </div>
                <div class="task-content">
                    <span class="task-text">${this.escapeHtml(task.text)}</span>
                    ${hasSubtasks ? `<span class="subtask-count">${completedSubtasks}/${subtaskCount} subtarefas</span>` : ''}
                </div>
                <div class="task-actions">
                    ${level === 0 ? `
                        <button class="task-btn add-subtask-btn" 
                                onclick="taskManager.showSubtaskInput(${task.id})"
                                aria-label="Adicionar subtarefa"
                                title="Adicionar subtarefa">
                            📋+
                        </button>
                    ` : ''}
                    <button class="task-btn delete-btn" 
                            onclick="taskManager.deleteTask(${task.id})"
                            aria-label="Excluir tarefa: ${this.escapeHtml(task.text)}"
                            title="Excluir tarefa">
                        🗑️
                    </button>
                </div>
            </div>
            ${level === 0 ? '<ul class="subtasks-list"></ul>' : ''}
        `;
        
        // Adicionar subtarefas se existirem
        if (hasSubtasks && level === 0) {
            const subtasksList = li.querySelector('.subtasks-list');
            task.subtasks.forEach(subtask => {
                const subtaskElement = this.createTaskElement(subtask, level + 1);
                subtasksList.appendChild(subtaskElement);
            });
        }
        
        return li;
    }

    // Criar cartão Kanban
    createKanbanCard(task) {
        const card = document.createElement('div');
        card.className = `kanban-card ${task.completed ? 'completed' : ''}`;
        card.setAttribute('data-task-id', task.id);
        card.draggable = true;
        
        const hasSubtasks = task.subtasks && task.subtasks.length > 0;
        const subtaskCount = hasSubtasks ? task.subtasks.length : 0;
        const completedSubtasks = hasSubtasks ? task.subtasks.filter(st => st.completed).length : 0;
        
        card.innerHTML = `
            <div class="task-main">
                <div class="task-checkbox ${task.completed ? 'checked' : ''}" 
                     onclick="taskManager.toggleTask(${task.id})"
                     role="checkbox" 
                     aria-checked="${task.completed}"
                     tabindex="0"
                     onkeypress="if(event.key==='Enter'||event.key===' ') taskManager.toggleTask(${task.id})">
                    ${task.completed ? '✓' : ''}
                </div>
                <div class="task-content">
                    <span class="task-text">${this.escapeHtml(task.text)}</span>
                    ${hasSubtasks ? `<span class="subtask-count">${completedSubtasks}/${subtaskCount} subtarefas</span>` : ''}
                </div>
                <div class="task-actions">
                    <button class="task-btn add-subtask-btn" 
                            onclick="taskManager.showSubtaskInput(${task.id})"
                            aria-label="Adicionar subtarefa"
                            title="Adicionar subtarefa">
                        📋+
                    </button>
                    <button class="task-btn delete-btn" 
                            onclick="taskManager.deleteTask(${task.id})"
                            aria-label="Excluir tarefa: ${this.escapeHtml(task.text)}"
                            title="Excluir tarefa">
                        🗑️
                    </button>
                </div>
            </div>
            <ul class="subtasks-list"></ul>
        `;
        
        // Adicionar subtarefas se existirem
        if (hasSubtasks) {
            const subtasksList = card.querySelector('.subtasks-list');
            task.subtasks.forEach(subtask => {
                const subtaskElement = this.createSubtaskElement(subtask);
                subtasksList.appendChild(subtaskElement);
            });
        }

        // Eventos de drag and drop
        card.addEventListener('dragstart', (e) => this.handleDragStart(e));
        card.addEventListener('dragend', (e) => this.handleDragEnd(e));
        
        return card;
    }

    // Criar elemento de subtarefa para Kanban
    createSubtaskElement(subtask) {
        const li = document.createElement('li');
        li.className = `subtask ${subtask.completed ? 'completed' : ''}`;
        li.setAttribute('data-task-id', subtask.id);
        
        li.innerHTML = `
            <div class="task-main">
                <div class="task-checkbox ${subtask.completed ? 'checked' : ''}" 
                     onclick="taskManager.toggleTask(${subtask.id})"
                     role="checkbox" 
                     aria-checked="${subtask.completed}"
                     tabindex="0"
                     onkeypress="if(event.key==='Enter'||event.key===' ') taskManager.toggleTask(${subtask.id})">
                    ${subtask.completed ? '✓' : ''}
                </div>
                <div class="task-content">
                    <span class="task-text">${this.escapeHtml(subtask.text)}</span>
                </div>
                <div class="task-actions">
                    <button class="task-btn delete-btn" 
                            onclick="taskManager.deleteTask(${subtask.id})"
                            aria-label="Excluir subtarefa: ${this.escapeHtml(subtask.text)}"
                            title="Excluir subtarefa">
                        🗑️
                    </button>
                </div>
            </div>
        `;
        
        return li;
    }

    // Eventos de Drag and Drop
    handleDragStart(e) {
        const taskId = parseInt(e.target.getAttribute('data-task-id'));
        this.draggedTask = this.findTaskById(taskId);
        e.target.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', e.target.outerHTML);
    }

    handleDragEnd(e) {
        e.target.classList.remove('dragging');
        this.draggedTask = null;
    }

    handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        e.currentTarget.classList.add('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('drag-over');
        
        if (!this.draggedTask) return;

        const column = e.currentTarget.closest('.kanban-column');
        const newStatus = column.getAttribute('data-status');
        
        if (this.draggedTask.status !== newStatus) {
            this.updateTaskStatus(this.draggedTask.id, newStatus);
        }
    }

    // Atualizar status da tarefa
    updateTaskStatus(taskId, newStatus) {
        const task = this.findTaskById(taskId);
        if (!task) return;

        task.status = newStatus;
        
        // Atualizar completed baseado no status
        if (newStatus === 'completed') {
            task.completed = true;
            task.completedAt = new Date().toISOString();
            
            // Marcar subtarefas como concluídas
            if (task.subtasks) {
                task.subtasks.forEach(subtask => {
                    subtask.completed = true;
                    subtask.status = 'completed';
                    subtask.completedAt = new Date().toISOString();
                });
            }
        } else {
            task.completed = false;
            task.completedAt = null;
            
            // Desmarcar subtarefas se a tarefa não está completa
            if (task.subtasks) {
                task.subtasks.forEach(subtask => {
                    subtask.completed = false;
                    subtask.status = 'not_started';
                    subtask.completedAt = null;
                });
            }
        }

        this.saveTasks();
        this.render();
        
        const statusMessages = {
            'not_started': 'Tarefa movida para Não Iniciado',
            'in_progress': 'Tarefa movida para Em Andamento',
            'completed': 'Tarefa movida para Finalizado 🎉'
        };
        
        this.showSuccessMessage(statusMessages[newStatus]);
    }

    // Atualizar estado vazio
    updateEmptyState() {
        const filteredTasks = this.getFilteredTasks();
        const isEmpty = filteredTasks.length === 0;
        
        // Só mostrar estado vazio na view de lista
        if (this.currentView === 'list') {
            this.elements.emptyState.classList.toggle('hidden', !isEmpty);
            
            if (isEmpty) {
                const messages = {
                    'all': 'Nenhuma tarefa encontrada.<br>Adicione sua primeira tarefa para começar!',
                    'pending': 'Parabéns! 🎉<br>Você não tem tarefas pendentes.',
                    'completed': 'Ainda não há tarefas concluídas.<br>Complete algumas tarefas para vê-las aqui!'
                };
                
                this.elements.emptyState.querySelector('p').innerHTML = messages[this.currentFilter];
            }
        } else {
            // Esconder estado vazio no Kanban
            this.elements.emptyState.classList.add('hidden');
        }
    }

    // Atualizar botão de limpar
    updateClearButton() {
        const hasCompleted = this.tasks.some(t => t.status === 'completed');
        this.elements.clearCompleted.disabled = !hasCompleted;
    }

    // Mostrar modal de confirmação
    showConfirmModal() {
        this.elements.confirmModal.classList.add('show');
        this.elements.confirmModal.setAttribute('aria-hidden', 'false');
        this.elements.confirmDelete.focus();
        document.body.style.overflow = 'hidden';
    }

    // Esconder modal de confirmação
    hideConfirmModal() {
        this.elements.confirmModal.classList.remove('show');
        this.elements.confirmModal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    // Mostrar mensagem de erro
    showInputError(message) {
        const input = this.elements.taskInput;
        input.style.borderColor = 'var(--danger-color)';
        input.placeholder = message;
        
        setTimeout(() => {
            input.style.borderColor = '';
            input.placeholder = 'Digite sua nova tarefa...';
        }, 3000);
    }

    // Mostrar mensagem de sucesso
    showSuccessMessage(message) {
        // Criar elemento de notificação
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--accent-color);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            z-index: 1001;
            animation: slideIn 0.3s ease-out;
            max-width: 300px;
            font-weight: 500;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remover após 3 segundos
        setTimeout(() => {
            notification.style.animation = 'fadeOut 0.3s ease-out forwards';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    // Escapar HTML para prevenir XSS
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Salvar tarefas no localStorage
    saveTasks() {
        try {
            const data = {
                tasks: this.tasks,
                taskIdCounter: this.taskIdCounter,
                lastSaved: new Date().toISOString()
            };
            localStorage.setItem('todoApp_tasks', JSON.stringify(data));
        } catch (error) {
            console.error('Erro ao salvar tarefas:', error);
            this.showInputError('Erro ao salvar dados. Verifique o espaço de armazenamento.');
        }
    }

    // Carregar tarefas do localStorage
    loadTasks() {
        try {
            const saved = localStorage.getItem('todoApp_tasks');
            if (saved) {
                const data = JSON.parse(saved);
                
                // Validar estrutura dos dados
                if (data.tasks && Array.isArray(data.tasks)) {
                    this.tasks = data.tasks.map(task => ({
                        id: task.id || this.taskIdCounter++,
                        text: task.text || '',
                        completed: Boolean(task.completed),
                        createdAt: task.createdAt || new Date().toISOString(),
                        completedAt: task.completedAt || null,
                        status: task.status || (task.completed ? 'completed' : 'not_started'),
                        subtasks: task.subtasks ? task.subtasks.map(st => ({
                            id: st.id || this.taskIdCounter++,
                            text: st.text || '',
                            completed: Boolean(st.completed),
                            createdAt: st.createdAt || new Date().toISOString(),
                            completedAt: st.completedAt || null,
                            status: st.status || (st.completed ? 'completed' : 'not_started'),
                            subtasks: [],
                            parentId: task.id
                        })) : [],
                        parentId: task.parentId || null
                    }));
                    
                    this.taskIdCounter = Math.max(
                        data.taskIdCounter || 1,
                        Math.max(...this.tasks.map(t => t.id), 0) + 1
                    );
                }
            }
        } catch (error) {
            console.error('Erro ao carregar tarefas:', error);
            this.showInputError('Erro ao carregar dados salvos');
        }
    }

    // Exportar dados para backup
    exportData() {
        const data = {
            tasks: this.tasks,
            exportDate: new Date().toISOString(),
            version: '1.0'
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `tarefas_backup_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showSuccessMessage('Backup criado com sucesso!');
    }

    // Obter estatísticas
    getStats() {
        const now = new Date();
        const today = now.toDateString();
        
        const stats = {
            total: this.tasks.length,
            completed: this.tasks.filter(t => t.status === 'completed').length,
            pending: this.tasks.filter(t => t.status !== 'completed').length,
            completedToday: this.tasks.filter(t => 
                t.status === 'completed' && t.completedAt && 
                new Date(t.completedAt).toDateString() === today
            ).length,
            createdToday: this.tasks.filter(t => 
                new Date(t.createdAt).toDateString() === today
            ).length
        };
        
        stats.completionRate = stats.total > 0 ? 
            Math.round((stats.completed / stats.total) * 100) : 0;
        
        return stats;
    }

    // Migrar dados existentes para incluir status
    migrateExistingTasks() {
        let needsMigration = false;
        
        const migrateTask = (task) => {
            if (!task.status) {
                task.status = task.completed ? 'completed' : 'not_started';
                needsMigration = true;
            }
            
            if (task.subtasks) {
                task.subtasks.forEach(migrateTask);
            }
        };

        this.tasks.forEach(migrateTask);
        
        if (needsMigration) {
            this.saveTasks();
            console.log('✅ Dados migrados para sistema Kanban');
        }
    }
}

// Inicializar aplicação quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    window.taskManager = new TaskManager();
    
    // Adicionar estilos para notificações
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(-20px); }
        }
    `;
    document.head.appendChild(style);
    
    // Log de inicialização
    console.log('📝 Lista de Tarefas inicializada com sucesso!');
    console.log('💾 Dados salvos automaticamente no localStorage');
});

// Salvar dados antes de sair da página
window.addEventListener('beforeunload', () => {
    if (window.taskManager) {
        window.taskManager.saveTasks();
    }
});

// Função global para acessar estatísticas (útil para debug)
window.getTaskStats = () => {
    if (window.taskManager) {
        const stats = window.taskManager.getStats();
        console.table(stats);
        return stats;
    }
    return null;
};