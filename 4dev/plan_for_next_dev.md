1. Убрать ошибки внутренней системы телеметрии ChromaDB
 ERROR:chromadb.telemetry.product.posthog:Failed to send telemetry event ClientCreateCollectionEvent: capture() takes 1 positional argument but 3 were given

 ERROR:chromadb.telemetry.product.posthog:Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument but 3 were given

2. Как улучшить обновление базы знаний без необходимости удаления? Реализовать проверку дубликатов?

 Как это можно сделать:
 При индексации каждого чанка мы должны добавлять в его метаданные путь к исходному файлу. Например: metadata={"source": "app/knowledge_base/my_document.md"}.

 Тогда процесс обновления для измененного файла будет выглядеть так:

 - Получить путь к измененному файлу (например, app/knowledge_base/my_document.md).
 - Выполнить в ChromaDB запрос на удаление всех векторов, у которых в метаданных source равен этому пути.
 - Прочитать новый, измененный файл, разбить его на чанки.
 - Добавить эти новые чанки в ChromaDB (опять же, с указанием пути в метаданных).

3. Отредактироварь:
 app/knowledge_base/prime_networking_my_portfolio_project_README.md

4. Собрать все планы по реализации в один подробный документ

5. Выпустить релиз - обновить репу

6. Развернуть бота на рендер или своём сервере

7. Реализовать выбор моделей Mistral