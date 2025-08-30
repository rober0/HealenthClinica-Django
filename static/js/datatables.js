import { DataTable } from 'simple-datatables';

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM Content Loaded - Initializing DataTables...");

    const paginationTable1 = document.getElementById("pagination-table");
    if (paginationTable1) {
        console.log("Initializing #pagination-table...");
        try {
            const dataTable1 = new DataTable(paginationTable1, {
                paging: true,
                searchable: false,
                sortable: true,
                perPage: 5,
                template: (options, dom) => `
                    <div class="${options.classes.container}"${options.scrollY.length ? ` style="height: ${options.scrollY}; overflow-Y: auto;"` : ""}>
                    </div>
                    <div class='${options.classes.bottom}'>
                        <nav class='${options.classes.pagination}'></nav>
                    </div>
                `
            });
            console.log("#pagination-table initialized successfully!", dataTable1);
        } catch (error) {
            console.error("Error initializing #pagination-table:", error);
        }
    } else {
        console.warn("#pagination-table element not found.");
    }

    const paginationTable2 = document.getElementById("pagination-table-2");
    if (paginationTable2) {
        console.log("Initializing #pagination-table-2...");
        try {
            const dataTable2 = new DataTable(paginationTable2, {
                paging: true,
                searchable: false,
                sortable: true,
                perPage: 5,
                template: (options, dom) => `
                    <div class="${options.classes.container}"${options.scrollY.length ? ` style="height: ${options.scrollY}; overflow-Y: auto;"` : ""}>
                    </div>
                    <div class='${options.classes.bottom}'>
                        <nav class="${options.classes.pagination}"></nav>
                    </div>
                `
            });
            console.log("#pagination-table-2 initialized successfully!", dataTable2);
        } catch (error) {
            console.error("Error initializing #pagination-table-2:", error);
        }
    } else {
        console.warn("#pagination-table-2 element not found.");
    }

    const sortingTable = document.getElementById("sorting-table");
    if (sortingTable) {
        console.log("Initializing #sorting-table...");
        try {
            const dataTable3 = new DataTable(sortingTable, {
                labels: {
                    placeholder: 'Pesquisar',
                    searchTitle: 'Pesquise na Tabela',
                    pageTitle: 'Página {page}',
                    perPage: 'Entradas por página',
                    noRows: 'Sem entradas encontradas',
                    info: 'Mostrando {start} de {end} em {rows} entradas',
                    noResults: 'Resultados não encontrados'
                },
                paging: true,
                perPage: 5,
                perPageSelect: [5, 10, 15, 20, 25],
                sortable: true,
                locale: 'pt-BR',
                numeric: true,
                caseFirst: 'false',
                ignorePunctuation: true,
                columns: [
                    {
                        select: 0,
                        sort: 'asc'
                    }
                ]
            });
            console.log("#sorting-table initialized successfully!", dataTable3);
        } catch (error) {
            console.error("Error initializing #sorting-table:", error);
        }
    } else {
        console.warn("#sorting-table element not found.");
    }
});