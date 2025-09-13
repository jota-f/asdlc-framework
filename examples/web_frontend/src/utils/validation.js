/**
 * 🛡️ Módulo de Validação - A-SDLC Framework
 * Centraliza todas as validações para evitar duplicação de código
 */

// ===== CONFIGURAÇÕES DE VALIDAÇÃO =====
const VALIDATION_CONFIG = {
    MAX_TASK_LENGTH: 100,
    MAX_SUB_TASK_LENGTH: 80
};

/**
 * ✅ Validar entrada de texto genérica
 * @param {string} text - Texto a validar
 * @param {number} maxLength - Comprimento máximo permitido
 * @param {Array} existingItems - Array de itens existentes para verificar duplicatas
 * @param {string} itemType - Tipo do item para mensagens de erro
 * @returns {Object} - Resultado da validação {isValid, message}
 */
export function validateTextInput(text, maxLength, existingItems = [], itemType = 'item') {
    if (!text || text.trim().length === 0) {
        return {
            isValid: false,
            message: `Digite um ${itemType} antes de adicionar`
        };
    }

    if (text.length > maxLength) {
        return {
            isValid: false,
            message: `${itemType.charAt(0).toUpperCase() + itemType.slice(1)} muito longo (máximo ${maxLength} caracteres)`
        };
    }

    // Verificar duplicatas
    const isDuplicate = existingItems.some(item => 
        (item.text || item.title).toLowerCase().trim() === text.toLowerCase().trim()
    );

    if (isDuplicate) {
        return {
            isValid: false,
            message: `Este ${itemType} já existe`
        };
    }

    return {
        isValid: true,
        message: ''
    };
}

/**
 * ✅ Validar entrada de tarefa
 * @param {string} text - Texto da tarefa
 * @param {Array} existingTasks - Tarefas existentes
 * @returns {Object} - Resultado da validação
 */
export function validateTaskInput(text, existingTasks = []) {
    return validateTextInput(text, VALIDATION_CONFIG.MAX_TASK_LENGTH, existingTasks, 'tarefa');
}

/**
 * ✅ Validar entrada de sub-tarefa
 * @param {string} text - Texto da sub-tarefa
 * @param {Array} existingSubTasks - Sub-tarefas existentes
 * @returns {Object} - Resultado da validação
 */
export function validateSubTaskInput(text, existingSubTasks = []) {
    return validateTextInput(text, VALIDATION_CONFIG.MAX_SUB_TASK_LENGTH, existingSubTasks, 'sub-tarefa');
}

/**
 * 🔢 Gerar ID único
 * @param {number} counter - Contador atual
 * @returns {number} - Novo ID
 */
export function generateId(counter) {
    return counter + 1;
}

/**
 * 🛡️ Escapar HTML para segurança
 * @param {string} text - Texto a escapar
 * @returns {string} - Texto escapado
 */
export function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
} 