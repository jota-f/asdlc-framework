/**
 * Testes Unitários - SubTask Component
 * Validação dos critérios de aceitação da story
 * Seguindo padrões A-SDLC de teste
 */

// ===== SIMULAÇÃO DE DOM PARA TESTES =====
class MockDOM {
    constructor() {
        this.storage = {};
        this.elements = new Map();
    }
    
    // Simular localStorage
    setItem(key, value) {
        this.storage[key] = value;
    }
    
    getItem(key) {
        return this.storage[key] || null;
    }
    
    removeItem(key) {
        delete this.storage[key];
    }
    
    // Simular elementos DOM
    createElement(tagName) {
        return {
            tagName: tagName.toUpperCase(),
            textContent: '',
            innerHTML: '',
            dataset: {},
            addEventListener: () => {},
            querySelector: () => null,
            setAttribute: () => {}
        };
    }
    
    querySelector(selector) {
        return this.elements.get(selector) || null;
    }
}

// ===== CONFIGURAÇÃO DE TESTE =====
const mockDOM = new MockDOM();

// Simular ambiente global
global.localStorage = mockDOM;
global.document = mockDOM;
global.console = {
    log: () => {},
    error: () => {},
    warn: () => {}
};

// ===== IMPORTAÇÃO DOS MÓDULOS TESTADOS =====
// Nota: Em ambiente real, usar import dinâmico ou sistema de módulos apropriado
const { saveSubTasks, getSubTasks, clearSubTasks, getSubTasksStats } = require('../utils/storage.js');
const { SubTask, SubTaskManager } = require('../components/SubTask.js');

// ===== TESTES DO STORAGE =====
describe('🧪 [Test Agent] Storage Utils - Sub Tarefas', () => {
    
    beforeEach(() => {
        // Limpar storage antes de cada teste
        mockDOM.storage = {};
        console.log('🔧 [Test] Limpando storage para teste...');
    });
    
    test('✅ Deve salvar sub tarefas no localStorage', () => {
        const subTasks = [
            { id: 1, parentTaskId: 1, title: 'Sub tarefa 1', completed: false },
            { id: 2, parentTaskId: 1, title: 'Sub tarefa 2', completed: true }
        ];
        
        const result = saveSubTasks(subTasks);
        
        expect(result).toBe(true);
        expect(mockDOM.storage['asdlc_sub_tasks']).toBeDefined();
        
        const savedData = JSON.parse(mockDOM.storage['asdlc_sub_tasks']);
        expect(savedData.subTasks).toEqual(subTasks);
        expect(savedData.version).toBe('1.0');
        
        console.log('✅ [Test] Salvamento de sub tarefas - PASSOU');
    });
    
    test('✅ Deve recuperar sub tarefas do localStorage', () => {
        const subTasks = [
            { id: 1, parentTaskId: 1, title: 'Sub tarefa teste', completed: false }
        ];
        
        // Preparar dados no storage
        const dataToSave = {
            subTasks: subTasks,
            lastUpdated: new Date().toISOString(),
            version: '1.0'
        };
        mockDOM.storage['asdlc_sub_tasks'] = JSON.stringify(dataToSave);
        
        const result = getSubTasks();
        
        expect(result).toEqual(subTasks);
        
        console.log('✅ [Test] Recuperação de sub tarefas - PASSOU');
    });
    
    test('✅ Deve retornar array vazio quando não há dados', () => {
        const result = getSubTasks();
        
        expect(Array.isArray(result)).toBe(true);
        expect(result.length).toBe(0);
        
        console.log('✅ [Test] Array vazio para storage limpo - PASSOU');
    });
    
    test('✅ Deve limpar todas as sub tarefas', () => {
        // Preparar dados
        mockDOM.storage['asdlc_sub_tasks'] = JSON.stringify({ subTasks: [] });
        
        const result = clearSubTasks();
        
        expect(result).toBe(true);
        expect(mockDOM.storage['asdlc_sub_tasks']).toBeUndefined();
        
        console.log('✅ [Test] Limpeza de sub tarefas - PASSOU');
    });
    
    test('✅ Deve calcular estatísticas corretamente', () => {
        const subTasks = [
            { id: 1, completed: true },
            { id: 2, completed: false },
            { id: 3, completed: true }
        ];
        
        // Salvar dados
        saveSubTasks(subTasks);
        
        const stats = getSubTasksStats();
        
        expect(stats.total).toBe(3);
        expect(stats.completed).toBe(2);
        expect(stats.pending).toBe(1);
        expect(stats.completionRate).toBe(67); // 2/3 = 67%
        
        console.log('✅ [Test] Cálculo de estatísticas - PASSOU');
    });
});

// ===== TESTES DO COMPONENTE SUBTASK =====
describe('🧪 [Test Agent] SubTask Component', () => {
    
    let subTask;
    const parentTaskId = 1;
    
    beforeEach(() => {
        mockDOM.storage = {};
        subTask = new SubTask(parentTaskId);
        console.log('🔧 [Test] Criando nova instância de SubTask...');
    });
    
    test('✅ Deve inicializar corretamente', () => {
        expect(subTask.parentTaskId).toBe(parentTaskId);
        expect(Array.isArray(subTask.subTasks)).toBe(true);
        expect(subTask.subTaskIdCounter).toBe(1);
        
        console.log('✅ [Test] Inicialização do SubTask - PASSOU');
    });
    
    test('✅ Deve adicionar nova sub tarefa', () => {
        const title = 'Nova sub tarefa teste';
        
        const result = subTask.addSubTask(title);
        
        expect(result).not.toBeNull();
        expect(result.title).toBe(title);
        expect(result.parentTaskId).toBe(parentTaskId);
        expect(result.completed).toBe(false);
        expect(subTask.subTasks.length).toBe(1);
        
        console.log('✅ [Test] Adição de sub tarefa - PASSOU');
    });
    
    test('✅ Deve rejeitar sub tarefa com título vazio', () => {
        const result = subTask.addSubTask('');
        
        expect(result).toBeNull();
        expect(subTask.subTasks.length).toBe(0);
        
        console.log('✅ [Test] Rejeição de título vazio - PASSOU');
    });
    
    test('✅ Deve rejeitar sub tarefa duplicada', () => {
        const title = 'Sub tarefa duplicada';
        
        // Adicionar primeira vez
        subTask.addSubTask(title);
        
        // Tentar adicionar novamente
        const result = subTask.addSubTask(title);
        
        expect(result).toBeNull();
        expect(subTask.subTasks.length).toBe(1);
        
        console.log('✅ [Test] Prevenção de duplicatas - PASSOU');
    });
    
    test('✅ Deve remover sub tarefa corretamente', () => {
        // Adicionar sub tarefa
        const subTaskAdded = subTask.addSubTask('Sub tarefa para remoção');
        
        // Remover
        const result = subTask.removeSubTask(subTaskAdded.id);
        
        expect(result).toBe(true);
        expect(subTask.subTasks.length).toBe(0);
        
        console.log('✅ [Test] Remoção de sub tarefa - PASSOU');
    });
    
    test('✅ Deve alternar status de conclusão', () => {
        // Adicionar sub tarefa
        const subTaskAdded = subTask.addSubTask('Sub tarefa toggle');
        const originalStatus = subTaskAdded.completed;
        
        // Alternar status
        const result = subTask.toggleSubTask(subTaskAdded.id);
        
        expect(result).toBe(true);
        expect(subTaskAdded.completed).toBe(!originalStatus);
        
        console.log('✅ [Test] Alternância de status - PASSOU');
    });
    
    test('✅ Deve calcular estatísticas corretamente', () => {
        // Adicionar sub tarefas
        const subTask1 = subTask.addSubTask('Sub 1');
        const subTask2 = subTask.addSubTask('Sub 2');
        const subTask3 = subTask.addSubTask('Sub 3');
        
        // Marcar algumas como concluídas
        subTask.toggleSubTask(subTask1.id);
        subTask.toggleSubTask(subTask2.id);
        
        const stats = subTask.getStats();
        
        expect(stats.total).toBe(3);
        expect(stats.completed).toBe(2);
        expect(stats.pending).toBe(1);
        expect(stats.completionRate).toBe(67);
        
        console.log('✅ [Test] Estatísticas do componente - PASSOU');
    });
});

// ===== TESTES DO GERENCIADOR =====
describe('🧪 [Test Agent] SubTaskManager', () => {
    
    let manager;
    
    beforeEach(() => {
        mockDOM.storage = {};
        manager = new SubTaskManager();
        console.log('🔧 [Test] Criando nova instância de SubTaskManager...');
    });
    
    test('✅ Deve criar instâncias únicas por tarefa pai', () => {
        const instance1 = manager.getSubTaskInstance(1);
        const instance2 = manager.getSubTaskInstance(2);
        const instance1Again = manager.getSubTaskInstance(1);
        
        expect(instance1).not.toBe(instance2);
        expect(instance1).toBe(instance1Again);
        
        console.log('✅ [Test] Instâncias únicas por tarefa - PASSOU');
    });
});

// ===== EXECUÇÃO DOS TESTES =====
console.log('🚀 [Test Agent] Iniciando bateria de testes...');

// Função simples de teste (substituiria framework como Jest)
function expect(actual) {
    return {
        toBe: (expected) => {
            if (actual !== expected) {
                throw new Error(`Expected ${expected}, got ${actual}`);
            }
        },
        toEqual: (expected) => {
            if (JSON.stringify(actual) !== JSON.stringify(expected)) {
                throw new Error(`Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
            }
        },
        toBeNull: () => {
            if (actual !== null) {
                throw new Error(`Expected null, got ${actual}`);
            }
        },
        toBeDefined: () => {
            if (actual === undefined) {
                throw new Error('Expected value to be defined');
            }
        },
        toBeUndefined: () => {
            if (actual !== undefined) {
                throw new Error(`Expected undefined, got ${actual}`);
            }
        }
    };
}

function describe(description, testFn) {
    console.log(`\n📋 ${description}`);
    try {
        testFn();
        console.log(`✅ ${description} - TODOS OS TESTES PASSARAM`);
    } catch (error) {
        console.error(`❌ ${description} - ERRO:`, error.message);
    }
}

function test(description, testFn) {
    try {
        testFn();
    } catch (error) {
        console.error(`❌ ${description} - FALHOU:`, error.message);
        throw error;
    }
}

function beforeEach(setupFn) {
    setupFn();
}

// Executar testes se não estiver em ambiente de módulo
if (typeof module !== 'undefined') {
    console.log('📊 [Test Agent] Testes criados e prontos para execução!');
    console.log('🎯 [Test Agent] Para executar: node src/tests/SubTask.test.js');
}