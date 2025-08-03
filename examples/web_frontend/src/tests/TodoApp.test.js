/**
 * 🧪 Testes Automatizados - TodoApp
 * Validação dos critérios de aceitação da story 20250803_123038_kanbam_kanbam.md
 */

import { validateTaskInput, validateSubTaskInput, escapeHtml } from '../utils/validation.js';

/**
 * 🧪 Suite de testes para TodoApp
 */
class TodoAppTestSuite {
    constructor() {
        this.passedTests = 0;
        this.failedTests = 0;
        this.totalTests = 0;
    }

    /**
     * ✅ Executar teste
     * @param {string} testName - Nome do teste
     * @param {Function} testFn - Função do teste
     */
    test(testName, testFn) {
        this.totalTests++;
        try {
            testFn();
            this.passedTests++;
            console.log(`✅ ${testName}`);
        } catch (error) {
            this.failedTests++;
            console.error(`❌ ${testName}: ${error.message}`);
        }
    }

    /**
     * 📊 Executar todos os testes
     */
    runAllTests() {
        console.log('🧪 Iniciando testes do TodoApp...\n');

        // ===== TESTES DE VALIDAÇÃO =====
        this.test('Validar entrada de tarefa válida', () => {
            const result = validateTaskInput('Nova tarefa', []);
            if (!result.isValid) throw new Error('Tarefa válida foi rejeitada');
        });

        this.test('Rejeitar tarefa vazia', () => {
            const result = validateTaskInput('', []);
            if (result.isValid) throw new Error('Tarefa vazia foi aceita');
        });

        this.test('Rejeitar tarefa muito longa', () => {
            const longTask = 'a'.repeat(101);
            const result = validateTaskInput(longTask, []);
            if (result.isValid) throw new Error('Tarefa muito longa foi aceita');
        });

        this.test('Rejeitar tarefa duplicada', () => {
            const existingTasks = [{ text: 'Tarefa existente' }];
            const result = validateTaskInput('Tarefa existente', existingTasks);
            if (result.isValid) throw new Error('Tarefa duplicada foi aceita');
        });

        // ===== TESTES DE SUB-TAREFAS =====
        this.test('Validar entrada de sub-tarefa válida', () => {
            const result = validateSubTaskInput('Nova sub-tarefa', []);
            if (!result.isValid) throw new Error('Sub-tarefa válida foi rejeitada');
        });

        this.test('Rejeitar sub-tarefa vazia', () => {
            const result = validateSubTaskInput('', []);
            if (result.isValid) throw new Error('Sub-tarefa vazia foi aceita');
        });

        // ===== TESTES DE SEGURANÇA =====
        this.test('Escapar HTML malicioso', () => {
            const maliciousInput = '<script>alert("xss")</script>';
            const escaped = escapeHtml(maliciousInput);
            if (escaped.includes('<script>')) {
                throw new Error('HTML malicioso não foi escapado corretamente');
            }
        });

        // ===== TESTES DE PERFORMANCE =====
        this.test('Validar performance de validação', () => {
            const start = performance.now();
            for (let i = 0; i < 1000; i++) {
                validateTaskInput(`Tarefa ${i}`, []);
            }
            const end = performance.now();
            const duration = end - start;
            
            if (duration > 50) { // Máximo 50ms para 1000 validações
                throw new Error(`Performance muito lenta: ${duration.toFixed(2)}ms`);
            }
        });

        // ===== TESTES DE ESTABILIDADE =====
        this.test('Validar entrada com caracteres especiais', () => {
            const specialChars = 'Tarefa com ç, ã, é, í, ó, ú, ñ, á, à, â, ê, î, ô, û';
            const result = validateTaskInput(specialChars, []);
            if (!result.isValid) throw new Error('Caracteres especiais foram rejeitados');
        });

        this.test('Validar entrada com números', () => {
            const numericTask = 'Tarefa 123 com números 456';
            const result = validateTaskInput(numericTask, []);
            if (!result.isValid) throw new Error('Números foram rejeitados');
        });

        // ===== RELATÓRIO FINAL =====
        this.printReport();
    }

    /**
     * 📊 Imprimir relatório de testes
     */
    printReport() {
        console.log('\n📊 RELATÓRIO DE TESTES');
        console.log('========================');
        console.log(`✅ Testes aprovados: ${this.passedTests}`);
        console.log(`❌ Testes falharam: ${this.failedTests}`);
        console.log(`📋 Total de testes: ${this.totalTests}`);
        
        const successRate = (this.passedTests / this.totalTests) * 100;
        console.log(`📈 Taxa de sucesso: ${successRate.toFixed(1)}%`);
        
        if (this.failedTests === 0) {
            console.log('🎉 TODOS OS TESTES PASSARAM!');
        } else {
            console.log('⚠️ Alguns testes falharam. Verifique os erros acima.');
        }
    }
}

// ===== EXECUTAR TESTES =====
if (typeof window !== 'undefined') {
    // Executar no browser
    window.runTodoAppTests = () => {
        const testSuite = new TodoAppTestSuite();
        testSuite.runAllTests();
    };
    
    // Executar automaticamente se estiver em modo de desenvolvimento
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        setTimeout(() => {
            console.log('🧪 Executando testes automaticamente...');
            window.runTodoAppTests();
        }, 1000);
    }
} else {
    // Executar no Node.js
    const testSuite = new TodoAppTestSuite();
    testSuite.runAllTests();
} 