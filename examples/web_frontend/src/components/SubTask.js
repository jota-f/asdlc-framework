/**
 * Componente SubTask - A-SDLC
 * Sistema de gerenciamento de sub-tarefas
 * Adaptado para JavaScript vanilla seguindo padrões A-SDLC
 */

import { saveSubTasks, getSubTasks } from '../utils/storage.js';

// ===== CONFIGURAÇÕES DO COMPONENTE =====
const SUB_TASK_CONFIG = {
    MAX_SUB_TASK_LENGTH: 80,
    CONTAINER_CLASS: 'sub-task-container',
    ITEM_CLASS: 'sub-task-item'
};

/**
 * 🎯 Classe SubTask para gerenciamento de sub-tarefas
 */
export class SubTask {
    constructor(parentTaskId) {
        this.parentTaskId = parentTaskId;
        this.subTasks = [];
        this.subTaskIdCounter = 1;
        
        this.init();
    }
    
    /**
     * 🚀 Inicializar componente
     */
    init() {
        console.log('🔧 [SubTask] Inicializando componente para tarefa:', this.parentTaskId);
        
        this.loadSubTasks();
        this.setupSubTaskIdCounter();
        
        console.log('✅ [SubTask] Componente inicializado com sucesso');
    }
    
    /**
     * 📂 Carregar sub tarefas do storage
     */
    loadSubTasks() {
        try {
            const allSubTasks = getSubTasks();
            this.subTasks = allSubTasks.filter(subTask => subTask.parentTaskId === this.parentTaskId);
            
            console.log('📋 [SubTask] Sub tarefas carregadas:', this.subTasks.length);
            
        } catch (error) {
            console.error('❌ [SubTask] Erro ao carregar sub tarefas:', error);
            this.subTasks = [];
        }
    }
    
    /**
     * 🔢 Configurar contador de IDs
     */
    setupSubTaskIdCounter() {
        if (this.subTasks.length > 0) {
            this.subTaskIdCounter = Math.max(...this.subTasks.map(subTask => subTask.id)) + 1;
        }
    }
    
    /**
     * ➕ Adicionar nova sub tarefa
     * @param {string} title - Título da sub tarefa
     * @returns {Object|null} - Sub tarefa criada ou null em caso de erro
     */
    addSubTask(title) {
        try {
            console.log('🔧 [SubTask] Adicionando nova sub tarefa:', title);
            
            // Validar entrada
            if (!this.validateSubTaskInput(title)) {
                return null;
            }
            
            // Criar nova sub tarefa
            const newSubTask = {
                id: this.generateSubTaskId(),
                parentTaskId: this.parentTaskId,
                title: title.trim(),
                completed: false,
                createdAt: new Date().toISOString(),
                completedAt: null
            };
            
            // Adicionar à lista local
            this.subTasks.push(newSubTask);
            
            // Salvar no storage
            this.saveAllSubTasks();
            
            console.log('✅ [SubTask] Sub tarefa adicionada:', newSubTask);
            return newSubTask;
            
        } catch (error) {
            console.error('❌ [SubTask] Erro ao adicionar sub tarefa:', error);
            return null;
        }
    }
    
    /**
     * 🗑️ Remover sub tarefa
     * @param {number} subTaskId - ID da sub tarefa a remover
     * @returns {boolean} - Sucesso da operação
     */
    removeSubTask(subTaskId) {
        try {
            console.log('🔧 [SubTask] Removendo sub tarefa:', subTaskId);
            
            const index = this.subTasks.findIndex(subTask => subTask.id === subTaskId);
            
            if (index === -1) {
                console.warn('⚠️ [SubTask] Sub tarefa não encontrada:', subTaskId);
                return false;
            }
            
            // Remover da lista local
            this.subTasks.splice(index, 1);
            
            // Salvar no storage
            this.saveAllSubTasks();
            
            console.log('✅ [SubTask] Sub tarefa removida com sucesso');
            return true;
            
        } catch (error) {
            console.error('❌ [SubTask] Erro ao remover sub tarefa:', error);
            return false;
        }
    }
    
    /**
     * ✅ Alternar status de conclusão da sub tarefa
     * @param {number} subTaskId - ID da sub tarefa
     * @returns {boolean} - Sucesso da operação
     */
    toggleSubTask(subTaskId) {
        try {
            console.log('🔧 [SubTask] Alternando status da sub tarefa:', subTaskId);
            
            const subTask = this.subTasks.find(st => st.id === subTaskId);
            
            if (!subTask) {
                console.warn('⚠️ [SubTask] Sub tarefa não encontrada:', subTaskId);
                return false;
            }
            
            // Alternar status
            subTask.completed = !subTask.completed;
            subTask.completedAt = subTask.completed ? new Date().toISOString() : null;
            
            // Salvar no storage
            this.saveAllSubTasks();
            
            console.log('✅ [SubTask] Status alternado:', subTask);
            return true;
            
        } catch (error) {
            console.error('❌ [SubTask] Erro ao alternar sub tarefa:', error);
            return false;
        }
    }
    
    /**
     * 📊 Obter estatísticas das sub tarefas
     * @returns {Object} - Estatísticas
     */
    getStats() {
        const total = this.subTasks.length;
        const completed = this.subTasks.filter(subTask => subTask.completed).length;
        const pending = total - completed;
        
        return {
            total,
            completed,
            pending,
            completionRate: total > 0 ? Math.round((completed / total) * 100) : 0
        };
    }
    
    /**
     * 🎨 Renderizar HTML das sub tarefas
     * @returns {string} - HTML das sub tarefas
     */
    renderSubTasks() {
        if (this.subTasks.length === 0) {
            return `
                <div class="sub-task-empty">
                    <p>Nenhuma sub tarefa ainda</p>
                </div>
            `;
        }
        
        const subTasksHtml = this.subTasks.map(subTask => `
            <div class="sub-task-item ${subTask.completed ? 'completed' : ''}" data-sub-task-id="${subTask.id}">
                <input 
                    type="checkbox" 
                    class="sub-task-checkbox" 
                    ${subTask.completed ? 'checked' : ''}
                    onchange="window.subTaskManager.toggleSubTask(${this.parentTaskId}, ${subTask.id})"
                    aria-label="Marcar sub tarefa como ${subTask.completed ? 'pendente' : 'concluída'}"
                >
                <span class="sub-task-title" title="${this.escapeHtml(subTask.title)}">
                    ${this.escapeHtml(subTask.title)}
                </span>
                <button 
                    class="sub-task-remove-btn"
                    onclick="window.subTaskManager.removeSubTask(${this.parentTaskId}, ${subTask.id})"
                    aria-label="Remover sub tarefa"
                    title="Remover sub tarefa"
                >
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');
        
        return `
            <div class="sub-task-list">
                ${subTasksHtml}
            </div>
        `;
    }
    
    /**
     * 🎨 Renderizar formulário de adição
     * @returns {string} - HTML do formulário
     */
    renderAddForm() {
        return `
            <div class="sub-task-add-form">
                <div class="sub-task-input-group">
                    <input 
                        type="text" 
                        class="sub-task-input" 
                        placeholder="Adicionar sub tarefa..."
                        maxlength="${SUB_TASK_CONFIG.MAX_SUB_TASK_LENGTH}"
                        data-parent-task-id="${this.parentTaskId}"
                    >
                    <button 
                        class="sub-task-add-btn"
                        data-parent-task-id="${this.parentTaskId}"
                        onclick="window.subTaskManager.addSubTaskFromInput(${this.parentTaskId})"
                        title="Adicionar sub tarefa"
                    >
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
            </div>
        `;
    }
    
    /**
     * 💾 Salvar todas as sub tarefas no storage
     */
    saveAllSubTasks() {
        try {
            // Obter todas as sub tarefas de todos os pais
            const allSubTasks = getSubTasks();
            
            // Filtrar sub tarefas de outras tarefas pai
            const otherSubTasks = allSubTasks.filter(subTask => subTask.parentTaskId !== this.parentTaskId);
            
            // Combinar com as sub tarefas atuais
            const updatedSubTasks = [...otherSubTasks, ...this.subTasks];
            
            // Salvar no storage
            saveSubTasks(updatedSubTasks);
            
        } catch (error) {
            console.error('❌ [SubTask] Erro ao salvar todas as sub tarefas:', error);
        }
    }
    
    /**
     * ✅ Validar entrada de sub tarefa
     * @param {string} title - Título a validar
     * @returns {boolean} - Válido ou não
     */
    validateSubTaskInput(title) {
        if (!title || title.trim().length === 0) {
            console.warn('⚠️ [SubTask] Título vazio');
            return false;
        }
        
        if (title.length > SUB_TASK_CONFIG.MAX_SUB_TASK_LENGTH) {
            console.warn('⚠️ [SubTask] Título muito longo');
            return false;
        }
        
        // Verificar duplicatas
        const isDuplicate = this.subTasks.some(subTask => 
            subTask.title.toLowerCase().trim() === title.toLowerCase().trim()
        );
        
        if (isDuplicate) {
            console.warn('⚠️ [SubTask] Sub tarefa duplicada');
            return false;
        }
        
        return true;
    }
    
    /**
     * 🔢 Gerar ID único para sub tarefa
     * @returns {number} - ID único
     */
    generateSubTaskId() {
        return this.subTaskIdCounter++;
    }
    
    /**
     * 🛡️ Escapar HTML para segurança
     * @param {string} text - Texto a escapar
     * @returns {string} - Texto escapado
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

/**
 * 🎯 Gerenciador global de sub tarefas
 */
export class SubTaskManager {
    constructor() {
        this.subTaskInstances = new Map();
        console.log('🚀 [SubTaskManager] Inicializado');
    }
    
    /**
     * 📋 Obter ou criar instância de SubTask para uma tarefa
     * @param {number} parentTaskId - ID da tarefa pai
     * @returns {SubTask} - Instância do SubTask
     */
    getSubTaskInstance(parentTaskId) {
        if (!this.subTaskInstances.has(parentTaskId)) {
            this.subTaskInstances.set(parentTaskId, new SubTask(parentTaskId));
        }
        return this.subTaskInstances.get(parentTaskId);
    }
    
    /**
     * ➕ Adicionar sub tarefa via input
     * @param {number} parentTaskId - ID da tarefa pai
     */
    addSubTaskFromInput(parentTaskId) {
        try {
            console.log('🔧 [SubTaskManager] Tentando adicionar sub tarefa para parent:', parentTaskId);
            
            const input = document.querySelector(`input[data-parent-task-id="${parentTaskId}"]`);
            if (!input) {
                console.error('❌ [SubTaskManager] Input não encontrado para parent:', parentTaskId);
                return;
            }
            
            const title = input.value.trim();
            console.log('🔧 [SubTaskManager] Título da sub tarefa:', title);
            
            if (!title) {
                console.warn('⚠️ [SubTaskManager] Título vazio, não adicionando');
                return;
            }
            
            const subTaskInstance = this.getSubTaskInstance(parentTaskId);
            
            if (subTaskInstance.addSubTask(title)) {
                input.value = '';
                this.refreshSubTaskDisplay(parentTaskId);
                console.log('✅ [SubTaskManager] Sub tarefa adicionada com sucesso');
            } else {
                console.error('❌ [SubTaskManager] Falha ao adicionar sub tarefa');
            }
        } catch (error) {
            console.error('❌ [SubTaskManager] Erro em addSubTaskFromInput:', error);
        }
    }
    
    /**
     * 🗑️ Remover sub tarefa
     * @param {number} parentTaskId - ID da tarefa pai
     * @param {number} subTaskId - ID da sub tarefa
     */
    removeSubTask(parentTaskId, subTaskId) {
        const subTaskInstance = this.getSubTaskInstance(parentTaskId);
        
        if (subTaskInstance.removeSubTask(subTaskId)) {
            this.refreshSubTaskDisplay(parentTaskId);
        }
    }
    
    /**
     * ✅ Alternar sub tarefa
     * @param {number} parentTaskId - ID da tarefa pai
     * @param {number} subTaskId - ID da sub tarefa
     */
    toggleSubTask(parentTaskId, subTaskId) {
        const subTaskInstance = this.getSubTaskInstance(parentTaskId);
        
        if (subTaskInstance.toggleSubTask(subTaskId)) {
            this.refreshSubTaskDisplay(parentTaskId);
        }
    }
    
    /**
     * 🔄 Atualizar exibição das sub tarefas
     * @param {number} parentTaskId - ID da tarefa pai
     */
    refreshSubTaskDisplay(parentTaskId) {
        try {
            console.log('🔧 [SubTaskManager] Atualizando display para parent:', parentTaskId);
            
            const container = document.querySelector(`[data-task-id="${parentTaskId}"] .sub-task-container`);
            console.log('🔧 [Debug] Container encontrado:', !!container);
            
            if (container) {
                const subTaskInstance = this.getSubTaskInstance(parentTaskId);
                const subTasksHtml = subTaskInstance.renderSubTasks();
                const addFormHtml = subTaskInstance.renderAddForm();
                
                console.log('🔧 [Debug] SubTasks HTML length:', subTasksHtml.length);
                console.log('🔧 [Debug] AddForm HTML length:', addFormHtml.length);
                
                const fullHtml = subTasksHtml + addFormHtml;
                container.innerHTML = fullHtml;
                
                console.log('✅ [SubTaskManager] Container atualizado com HTML');
                console.log('🔧 [Debug] HTML completo:', fullHtml);
            } else {
                console.error('❌ [SubTaskManager] Container não encontrado para parent:', parentTaskId);
            }
        } catch (error) {
            console.error('❌ [SubTaskManager] Erro em refreshSubTaskDisplay:', error);
        }
    }
}