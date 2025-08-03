/**
 * 📊 Componente Kanban - A-SDLC Framework
 * Sistema de gerenciamento visual de tarefas com drag & drop
 * Desenvolvido seguindo EXATAMENTE as especificações da story 20250803_123038_kanbam_kanbam.md
 */

const { useState, useEffect } = React;

const Kanban = () => {
    const [tasks, setTasks] = useState({
        todo: [],
        inProgress: [],
        done: []
    });

    const [dragOverColumn, setDragOverColumn] = useState(null);
    const [draggedTaskId, setDraggedTaskId] = useState(null);

    // Sincronizar com as tarefas do TodoApp
    useEffect(() => {
        const waitForTodoApp = () => {
            // Verificar se o DOM está completamente carregado
            if (document.readyState === 'complete') {
                if (window.todoApp && window.todoApp.tasks) {
                    console.log('✅ TodoApp encontrado após DOM completo!');
                    console.log('🔍 Debug - window.todoApp:', window.todoApp);
                    console.log('🔍 Debug - window.todoApp.tasks:', window.todoApp.tasks);
                    updateKanbanTasks();
                    return true;
                } else {
                    console.log('⚠️ TodoApp não encontrado mesmo com DOM completo');
                    console.log('🔍 Debug - window.todoApp:', window.todoApp);
                    return false;
                }
            } else {
                console.log('⏳ DOM ainda não completo, aguardando...');
                return false;
            }
        };

        const updateKanbanTasks = () => {
            if (window.todoApp && window.todoApp.tasks) {
                const allTasks = window.todoApp.tasks;
                const filteredTasks = window.todoApp.getFilteredTasks ? window.todoApp.getFilteredTasks() : allTasks;
                
                console.log('🔍 Debug - TodoApp tasks:', allTasks);
                console.log('🔍 Debug - Filtered tasks:', filteredTasks);
                
                // Distribuir tarefas baseado em status (se existir) ou completed
                const kanbanTasks = {
                    todo: filteredTasks.filter(task => !task.completed && !task.status),
                    inProgress: filteredTasks.filter(task => task.status === 'inProgress' || task.status === 'progress'),
                    done: filteredTasks.filter(task => task.completed)
                };
                
                setTasks(kanbanTasks);
                console.log('🔄 Kanban sincronizado com TodoApp:', kanbanTasks);
                console.log('🔍 Debug - Todo tasks count:', kanbanTasks.todo.length);
                console.log('🔍 Debug - InProgress tasks count:', kanbanTasks.inProgress.length);
                console.log('🔍 Debug - Done tasks count:', kanbanTasks.done.length);
            }
        };

        // Aguardar DOM completo
        if (document.readyState === 'complete') {
            waitForTodoApp();
        } else {
            window.addEventListener('load', waitForTodoApp);
        }

        // Observar mudanças no TodoApp após inicialização
        const interval = setInterval(() => {
            if (window.todoApp && window.todoApp.tasks) {
                updateKanbanTasks();
            }
        }, 1000);
        
        return () => {
            clearInterval(interval);
            window.removeEventListener('load', waitForTodoApp);
        };
    }, []);

    const handleDrop = (status, e) => {
        e.preventDefault();
        e.stopPropagation();
        
        console.log('🎯 handleDrop chamado para status:', status);
        console.log('🎯 dataTransfer:', e.dataTransfer);
        
        const taskId = e.dataTransfer.getData('text/plain');
        console.log('🎯 taskId extraído:', taskId);
        
        if (!taskId) {
            console.log('❌ Nenhum taskId encontrado no dataTransfer');
            setDragOverColumn(null);
            setDraggedTaskId(null);
            return;
        }

        console.log(`🎯 Tentando mover tarefa ${taskId} para ${status}`);

        // Encontrar a tarefa em todas as colunas
        let taskToMove = null;
        let sourceStatus = null;
        
        Object.keys(tasks).forEach(key => {
            const task = tasks[key].find(t => t.id == taskId); // Use == para comparação flexível
            if (task) {
                taskToMove = task;
                sourceStatus = key;
                console.log(`✅ Tarefa encontrada em ${key}:`, task);
            }
        });

        if (!taskToMove) {
            console.log('❌ Tarefa não encontrada para mover');
            setDragOverColumn(null);
            setDraggedTaskId(null);
            return;
        }

        console.log(`✅ Tarefa encontrada: ${taskToMove.title || taskToMove.text} de ${sourceStatus}`);

        // Atualizar o status da tarefa no TodoApp
        if (window.todoApp && window.todoApp.toggleTask) {
            // Mapear status do kanban para completed e status
            if (status === 'done' && !taskToMove.completed) {
                // Marcar como concluída
                window.todoApp.toggleTask(taskToMove.id);
                console.log('🔄 Marcando tarefa como concluída no TodoApp');
            } else if (status === 'todo' && (taskToMove.completed || taskToMove.status)) {
                // Voltar para pendente
                if (taskToMove.completed) {
                    window.todoApp.toggleTask(taskToMove.id);
                }
                // Remover status se existir
                if (taskToMove.status) {
                    window.todoApp.updateTaskStatus(taskToMove.id, null);
                }
                console.log('🔄 Marcando tarefa como pendente no TodoApp');
            } else if (status === 'inProgress' && !taskToMove.completed) {
                // Marcar como em andamento
                window.todoApp.updateTaskStatus(taskToMove.id, 'inProgress');
                console.log('🔄 Marcando tarefa como em andamento no TodoApp');
            }
        }

        // Remover da coluna de origem
        const updatedTasks = {
            ...tasks,
            [sourceStatus]: tasks[sourceStatus].filter(task => task.id != taskId), // Use !=
            [status]: [...tasks[status], taskToMove]
        };
        
        setTasks(updatedTasks);
        setDragOverColumn(null);
        setDraggedTaskId(null);
        
        console.log(`✅ Tarefa ${taskId} movida de ${sourceStatus} para ${status}`);
    };

    const dragOverHandler = (e) => {
        e.preventDefault();
        e.stopPropagation();
        console.log('🎯 dragOverHandler chamado');
    };

    const dragEnterHandler = (status) => {
        console.log(`🎯 dragEnterHandler chamado para: ${status}`);
        setDragOverColumn(status);
    };

    const dragLeaveHandler = (e) => {
        console.log('🎯 dragLeaveHandler chamado');
        // Só limpa se não estiver entrando em um filho
        if (!e.currentTarget.contains(e.relatedTarget)) {
            setDragOverColumn(null);
        }
    };

    const dragStartHandler = (taskId, e) => {
        console.log(`🔄 dragStartHandler chamado para taskId: ${taskId}`);
        console.log('🔄 e.target:', e.target);
        console.log('🔄 e.currentTarget:', e.currentTarget);
        
        e.dataTransfer.setData('text/plain', taskId.toString());
        e.dataTransfer.effectAllowed = 'move';
        setDraggedTaskId(taskId);
        
        console.log(`🔄 Iniciando arrasto da tarefa: ${taskId}`);
    };

    const dragEndHandler = () => {
        console.log('🔄 dragEndHandler chamado');
        setDragOverColumn(null);
        setDraggedTaskId(null);
    };

    return (
        <div className="kanban">
            <div 
                className={`column ${dragOverColumn === 'todo' ? 'drag-over' : ''}`}
                onDrop={(e) => handleDrop('todo', e)} 
                onDragOver={dragOverHandler}
                onDragEnter={() => dragEnterHandler('todo')}
                onDragLeave={dragLeaveHandler}
            >
                <h2>Não Iniciado</h2>
                {tasks.todo.map(task => (
                    <div 
                        key={task.id} 
                        draggable 
                        onDragStart={(e) => dragStartHandler(task.id, e)} 
                        onDragEnd={dragEndHandler}
                        className={`kanban-task ${draggedTaskId === task.id ? 'dragging' : ''}`}
                    >
                        {task.title || task.text}
                    </div>
                ))}
            </div>
            <div 
                className={`column ${dragOverColumn === 'inProgress' ? 'drag-over' : ''}`}
                onDrop={(e) => handleDrop('inProgress', e)} 
                onDragOver={dragOverHandler}
                onDragEnter={() => dragEnterHandler('inProgress')}
                onDragLeave={dragLeaveHandler}
            >
                <h2>Em Andamento</h2>
                {tasks.inProgress.map(task => (
                    <div 
                        key={task.id} 
                        draggable 
                        onDragStart={(e) => dragStartHandler(task.id, e)} 
                        onDragEnd={dragEndHandler}
                        className={`kanban-task ${draggedTaskId === task.id ? 'dragging' : ''}`}
                    >
                        {task.title || task.text}
                    </div>
                ))}
            </div>
            <div 
                className={`column ${dragOverColumn === 'done' ? 'drag-over' : ''}`}
                onDrop={(e) => handleDrop('done', e)} 
                onDragOver={dragOverHandler}
                onDragEnter={() => dragEnterHandler('done')}
                onDragLeave={dragLeaveHandler}
            >
                <h2>Finalizado</h2>
                {tasks.done.map(task => (
                    <div 
                        key={task.id} 
                        draggable 
                        onDragStart={(e) => dragStartHandler(task.id, e)} 
                        onDragEnd={dragEndHandler}
                        className={`kanban-task ${draggedTaskId === task.id ? 'dragging' : ''}`}
                    >
                        {task.title || task.text}
                    </div>
                ))}
            </div>
        </div>
    );
};

const kanbanRoot = document.getElementById('kanbanRoot');
if (kanbanRoot) {
    const root = ReactDOM.createRoot(kanbanRoot);
    root.render(<Kanban />);
    console.log('✅ Componente Kanban React renderizado com createRoot');
} 