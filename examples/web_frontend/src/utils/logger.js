/**
 * 📝 Módulo de Logging - A-SDLC Framework
 * Sistema de logging estruturado para melhor rastreabilidade
 */

// ===== NÍVEIS DE LOG =====
const LOG_LEVELS = {
    DEBUG: 'debug',
    INFO: 'info',
    WARN: 'warn',
    ERROR: 'error',
    SUCCESS: 'success'
};

// ===== EMOJIS POR AÇÃO =====
const LOG_EMOJIS = {
    INIT: '🚀',
    SUCCESS: '✅',
    ERROR: '❌',
    WARNING: '⚠️',
    INFO: 'ℹ️',
    DEBUG: '🔍',
    SYNC: '🔄',
    TASK: '📋',
    KANBAN: '📊',
    DRAG: '🎯',
    VALIDATION: '🛡️',
    STORAGE: '💾',
    UI: '🎨'
};

/**
 * 📝 Logger principal
 */
class Logger {
    constructor(module = 'App') {
        this.module = module;
    }

    /**
     * 🔍 Log de debug
     * @param {string} message - Mensagem
     * @param {any} data - Dados opcionais
     */
    debug(message, data = null) {
        this._log(LOG_LEVELS.DEBUG, LOG_EMOJIS.DEBUG, message, data);
    }

    /**
     * ℹ️ Log de informação
     * @param {string} message - Mensagem
     * @param {any} data - Dados opcionais
     */
    info(message, data = null) {
        this._log(LOG_LEVELS.INFO, LOG_EMOJIS.INFO, message, data);
    }

    /**
     * ✅ Log de sucesso
     * @param {string} message - Mensagem
     * @param {any} data - Dados opcionais
     */
    success(message, data = null) {
        this._log(LOG_LEVELS.SUCCESS, LOG_EMOJIS.SUCCESS, message, data);
    }

    /**
     * ⚠️ Log de aviso
     * @param {string} message - Mensagem
     * @param {any} data - Dados opcionais
     */
    warn(message, data = null) {
        this._log(LOG_LEVELS.WARN, LOG_EMOJIS.WARNING, message, data);
    }

    /**
     * ❌ Log de erro
     * @param {string} message - Mensagem
     * @param {any} data - Dados opcionais
     */
    error(message, data = null) {
        this._log(LOG_LEVELS.ERROR, LOG_EMOJIS.ERROR, message, data);
    }

    /**
     * 📝 Método interno de logging
     * @param {string} level - Nível do log
     * @param {string} emoji - Emoji do log
     * @param {string} message - Mensagem
     * @param {any} data - Dados opcionais
     */
    _log(level, emoji, message, data = null) {
        const timestamp = new Date().toISOString();
        const logMessage = `${emoji} [${this.module}] ${message}`;
        
        switch (level) {
            case LOG_LEVELS.DEBUG:
                console.debug(logMessage, data);
                break;
            case LOG_LEVELS.INFO:
                console.info(logMessage, data);
                break;
            case LOG_LEVELS.SUCCESS:
                console.log(logMessage, data);
                break;
            case LOG_LEVELS.WARN:
                console.warn(logMessage, data);
                break;
            case LOG_LEVELS.ERROR:
                console.error(logMessage, data);
                break;
        }
    }
}

/**
 * 🏭 Factory para criar loggers específicos
 * @param {string} module - Nome do módulo
 * @returns {Logger} - Instância do logger
 */
export function createLogger(module) {
    return new Logger(module);
}

/**
 * 📊 Logger específico para métricas de performance
 */
export class PerformanceLogger extends Logger {
    constructor() {
        super('Performance');
    }

    /**
     * ⏱️ Medir tempo de execução
     * @param {string} operation - Nome da operação
     * @param {Function} fn - Função a medir
     * @returns {any} - Resultado da função
     */
    async measureTime(operation, fn) {
        const start = performance.now();
        try {
            const result = await fn();
            const end = performance.now();
            const duration = end - start;
            
            this.success(`${operation} executada em ${duration.toFixed(2)}ms`);
            return result;
        } catch (error) {
            const end = performance.now();
            const duration = end - start;
            this.error(`${operation} falhou após ${duration.toFixed(2)}ms`, error);
            throw error;
        }
    }

    /**
     * 📈 Log de métrica
     * @param {string} metric - Nome da métrica
     * @param {number} value - Valor da métrica
     * @param {string} unit - Unidade da métrica
     */
    metric(metric, value, unit = '') {
        this.info(`${metric}: ${value}${unit}`);
    }
}

// ===== LOGGERS ESPECÍFICOS =====
export const appLogger = createLogger('TodoApp');
export const kanbanLogger = createLogger('Kanban');
export const taskLogger = createLogger('TaskManager');
export const storageLogger = createLogger('Storage');
export const performanceLogger = new PerformanceLogger(); 