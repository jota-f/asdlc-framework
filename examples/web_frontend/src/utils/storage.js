/**
 * Módulo de Armazenamento para Sub Tarefas - A-SDLC
 * Sistema de persistência específico para sub-tarefas
 * Seguindo padrões A-SDLC e terminologia padronizada
 */

// ===== CONFIGURAÇÕES DE ARMAZENAMENTO =====
const STORAGE_CONFIG = {
    SUB_TASKS_KEY: 'asdlc_sub_tasks',
    KANBAN_KEY: 'asdlc_kanban_tasks',
    VERSION: '1.0'
};

/**
 * 💾 Salva sub tarefas no localStorage
 * @param {Array} subTasks - Array de sub tarefas para salvar
 * @returns {boolean} - Sucesso da operação
 */
export const saveSubTasks = (subTasks) => {
    try {
        console.log('🔧 [Storage] Salvando sub tarefas no localStorage...');
        
        // Validar entrada
        if (!Array.isArray(subTasks)) {
            throw new Error('SubTasks deve ser um array');
        }
        
        const dataToSave = {
            subTasks: subTasks,
            lastUpdated: new Date().toISOString(),
            version: STORAGE_CONFIG.VERSION
        };
        
        localStorage.setItem(STORAGE_CONFIG.SUB_TASKS_KEY, JSON.stringify(dataToSave));
        
        console.log('✅ [Storage] Sub tarefas salvas com sucesso:', subTasks.length);
        return true;
        
    } catch (error) {
        console.error('❌ [Storage] Erro ao salvar sub tarefas:', error);
        return false;
    }
};

/**
 * 📂 Recupera sub tarefas do localStorage
 * @returns {Array} - Array de sub tarefas ou array vazio
 */
export const getSubTasks = () => {
    try {
        console.log('🔧 [Storage] Carregando sub tarefas do localStorage...');
        
        const savedData = localStorage.getItem(STORAGE_CONFIG.SUB_TASKS_KEY);
        
        if (!savedData) {
            console.log('📋 [Storage] Nenhuma sub tarefa salva encontrada');
            return [];
        }
        
        const parsedData = JSON.parse(savedData);
        
        // Validar estrutura dos dados
        if (parsedData && Array.isArray(parsedData.subTasks)) {
            console.log('✅ [Storage] Sub tarefas carregadas:', parsedData.subTasks.length);
            return parsedData.subTasks;
        } else {
            console.warn('⚠️ [Storage] Formato de dados inválido no localStorage');
            return [];
        }
        
    } catch (error) {
        console.error('❌ [Storage] Erro ao carregar sub tarefas:', error);
        return [];
    }
};

/**
 * 🗑️ Remove todas as sub tarefas do localStorage
 * @returns {boolean} - Sucesso da operação
 */
export const clearSubTasks = () => {
    try {
        console.log('🔧 [Storage] Limpando todas as sub tarefas...');
        
        localStorage.removeItem(STORAGE_CONFIG.SUB_TASKS_KEY);
        
        console.log('✅ [Storage] Sub tarefas limpas com sucesso');
        return true;
        
    } catch (error) {
        console.error('❌ [Storage] Erro ao limpar sub tarefas:', error);
        return false;
    }
};

/**
 * 📊 Obter estatísticas das sub tarefas
 * @returns {Object} - Estatísticas das sub tarefas
 */
export const getSubTasksStats = () => {
    try {
        const subTasks = getSubTasks();
        const total = subTasks.length;
        const completed = subTasks.filter(subTask => subTask.completed).length;
        const pending = total - completed;
        
        return {
            total,
            completed,
            pending,
            completionRate: total > 0 ? Math.round((completed / total) * 100) : 0
        };
        
    } catch (error) {
        console.error('❌ [Storage] Erro ao obter estatísticas:', error);
        return { total: 0, completed: 0, pending: 0, completionRate: 0 };
    }
};

// ===== FUNÇÕES KANBAN =====

/**
 * 💾 Salva estado do kanban no localStorage
 * @param {Object} kanbanState - Estado das tarefas do kanban
 * @returns {boolean} - Sucesso da operação
 */
export const saveKanbanState = (kanbanState) => {
    try {
        console.log('🔧 [Storage] Salvando estado do kanban no localStorage...');
        
        // Validar entrada
        if (!kanbanState || typeof kanbanState !== 'object') {
            throw new Error('Estado do kanban deve ser um objeto');
        }
        
        const dataToSave = {
            kanbanState: kanbanState,
            lastUpdated: new Date().toISOString(),
            version: STORAGE_CONFIG.VERSION
        };
        
        localStorage.setItem(STORAGE_CONFIG.KANBAN_KEY, JSON.stringify(dataToSave));
        
        console.log('✅ [Storage] Estado do kanban salvo com sucesso');
        return true;
        
    } catch (error) {
        console.error('❌ [Storage] Erro ao salvar estado do kanban:', error);
        return false;
    }
};

/**
 * 📂 Recupera estado do kanban do localStorage
 * @returns {Object|null} - Estado das tarefas do kanban ou null
 */
export const loadKanbanState = () => {
    try {
        console.log('🔧 [Storage] Carregando estado do kanban do localStorage...');
        
        const savedData = localStorage.getItem(STORAGE_CONFIG.KANBAN_KEY);
        
        if (!savedData) {
            console.log('📋 [Storage] Nenhum estado do kanban salvo encontrado');
            return null;
        }
        
        const parsedData = JSON.parse(savedData);
        
        // Validar estrutura dos dados
        if (parsedData && parsedData.kanbanState && typeof parsedData.kanbanState === 'object') {
            console.log('✅ [Storage] Estado do kanban carregado com sucesso');
            return parsedData.kanbanState;
        } else {
            console.warn('⚠️ [Storage] Formato de dados do kanban inválido no localStorage');
            return null;
        }
        
    } catch (error) {
        console.error('❌ [Storage] Erro ao carregar estado do kanban:', error);
        return null;
    }
};

/**
 * 🗑️ Remove estado do kanban do localStorage
 * @returns {boolean} - Sucesso da operação
 */
export const clearKanbanState = () => {
    try {
        console.log('🔧 [Storage] Limpando estado do kanban...');
        
        localStorage.removeItem(STORAGE_CONFIG.KANBAN_KEY);
        
        console.log('✅ [Storage] Estado do kanban limpo com sucesso');
        return true;
        
    } catch (error) {
        console.error('❌ [Storage] Erro ao limpar estado do kanban:', error);
        return false;
    }
};

/**
 * 📊 Obter estatísticas do kanban
 * @returns {Object} - Estatísticas das tarefas do kanban
 */
export const getKanbanStats = () => {
    try {
        const kanbanState = loadKanbanState();
        if (!kanbanState) {
            return { total: 0, todo: 0, inProgress: 0, done: 0 };
        }
        
        const todo = kanbanState.todo ? kanbanState.todo.length : 0;
        const inProgress = kanbanState.inProgress ? kanbanState.inProgress.length : 0;
        const done = kanbanState.done ? kanbanState.done.length : 0;
        const total = todo + inProgress + done;
        
        return {
            total,
            todo,
            inProgress,
            done,
            completionRate: total > 0 ? Math.round((done / total) * 100) : 0
        };
        
    } catch (error) {
        console.error('❌ [Storage] Erro ao obter estatísticas do kanban:', error);
        return { total: 0, todo: 0, inProgress: 0, done: 0, completionRate: 0 };
    }
};