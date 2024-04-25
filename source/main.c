#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 1024

int numaplicacoes;
typedef struct Aplicacao Aplicacao;

struct Aplicacao {
  int ID;
  char Label[MAX_LINE_LENGTH];
  char String_Entrada[MAX_LINE_LENGTH];
  char String_Saida[MAX_LINE_LENGTH];
  char String_backup[MAX_LINE_LENGTH];
  int ud;
  Aplicacao *fornece_dados_backp;
  int fd;
  Aplicacao *fornce_dados;
  int fdb;
  Aplicacao *usa_dados;
};

void escape_special_characters(const char *input, char *output) {
    int input_length = strlen(input);
    int output_index = 0;
    for (int i = 0; i < input_length; i++) {
        if (input[i] == '\\' || input[i] == '\"') {
            output[output_index++] = '\\'; // Adiciona uma barra invertida extra para escapar
        }
        output[output_index++] = input[i];
    }
    output[output_index] = '\0'; // Adiciona o caractere nulo ao final da string
}
//Baseparateste , Exemplo
int main() {

  FILE *stream = fopen("output/func_data.csv", "r");
  if (stream == NULL) {
    printf("Erro ao abrir o arquivo.\n");
    return 1;
  }

  char buffer[MAX_LINE_LENGTH];
  numaplicacoes = 0;
  Aplicacao *aplicacoes = NULL;
  fgets(buffer, sizeof(buffer), stream);
  while (fgets(buffer, sizeof(buffer), stream)) {
    buffer[strlen(buffer) - 1] = '\0';
    aplicacoes = realloc(aplicacoes, (numaplicacoes + 1) * sizeof(Aplicacao));
    if (aplicacoes == NULL) {
      printf("Erro ao realocar memória.\n");
      fclose(stream);
      return 1;
    }
    /*
    char *temp = strtok(buffer, ";");
    aplicacoes[numaplicacoes].ID = atoi(temp);
    temp = strtok(NULL, ";");
    strcpy(aplicacoes[numaplicacoes].Label, temp);
    temp = strtok(NULL, ";");
    strcpy(aplicacoes[numaplicacoes].String_Entrada, temp);
    temp = strtok(NULL, ";");
    if (temp != NULL)
      strcpy(aplicacoes[numaplicacoes].String_Saida, temp);
    else
      strcpy(aplicacoes[numaplicacoes].String_Saida, "");
    temp = strtok(NULL, ";");
    if (temp != NULL)
      strcpy(aplicacoes[numaplicacoes].String_backup, temp);
    else
      strcpy(aplicacoes[numaplicacoes].String_backup, "");
    */

    char *temp = strtok(buffer, ";");
    aplicacoes[numaplicacoes].ID = atoi(temp);
    temp = strtok(NULL, ";");
    strcpy(aplicacoes[numaplicacoes].Label, temp);
    temp = strtok(NULL, ";");
    strcpy(aplicacoes[numaplicacoes].String_Entrada, temp);
    temp = strtok(NULL, ";");
    if (temp != NULL)
      strcpy(aplicacoes[numaplicacoes].String_Saida, temp);
    else
      strcpy(aplicacoes[numaplicacoes].String_Saida, "");
    temp = strtok(NULL, ";");
    if (temp != NULL)
      strcpy(aplicacoes[numaplicacoes].String_backup, temp);
    else
      strcpy(aplicacoes[numaplicacoes].String_backup, "");

    aplicacoes[numaplicacoes].fd = 0;
    aplicacoes[numaplicacoes].ud = 0;
    aplicacoes[numaplicacoes].fdb = 0;
    aplicacoes[numaplicacoes].usa_dados = NULL;
    aplicacoes[numaplicacoes].fornce_dados = NULL;
    aplicacoes[numaplicacoes].fornece_dados_backp = NULL;
    /*
    printf("ID: %d, Label: %s, Entrada: %s, Saida: %s, Backup: %s\n",
           aplicacoes[numaplicacoes].ID, aplicacoes[numaplicacoes].Label,
           aplicacoes[numaplicacoes].String_Entrada,
           aplicacoes[numaplicacoes].String_Saida,
           aplicacoes[numaplicacoes].String_backup);
    */
    numaplicacoes++;
    free(temp);
  }

  for (int i = 0; i < numaplicacoes; i++) {
    for (int j = 0; j < numaplicacoes; j++) {

      if (i != j) {
        if (strcasecmp(aplicacoes[i].String_Saida, aplicacoes[j].String_Entrada) ==
            0) {
          aplicacoes[i].fornce_dados =
              realloc(aplicacoes[i].fornce_dados,
                      (aplicacoes[i].fd + 1) * sizeof(Aplicacao));
          aplicacoes[i].fornce_dados[aplicacoes[i].fd] = aplicacoes[j];
          aplicacoes[i].fd++;

          aplicacoes[j].usa_dados =
              realloc(aplicacoes[j].usa_dados,
                      (aplicacoes[j].ud + 1) * sizeof(Aplicacao));
          aplicacoes[j].usa_dados[aplicacoes[j].ud] = aplicacoes[i];
          aplicacoes[j].ud++;
        }
        if (strcasecmp(aplicacoes[i].String_backup, aplicacoes[j].String_Entrada) ==
            0) {
          aplicacoes[i].fornece_dados_backp =
              realloc(aplicacoes[i].fornece_dados_backp,
                      (aplicacoes[i].fdb + 1) * sizeof(Aplicacao));
          aplicacoes[i].fornece_dados_backp[aplicacoes[i].fdb] = aplicacoes[j];
          aplicacoes[i].fdb++;
          aplicacoes[j].usa_dados =
              realloc(aplicacoes[j].usa_dados,
                      (aplicacoes[j].ud + 1) * sizeof(Aplicacao));
          aplicacoes[j].usa_dados[aplicacoes[j].ud] = aplicacoes[i];
          aplicacoes[j].ud++;
        }
      }
    }
  }


    FILE *file = fopen("output/grafo.dot", "w");
if (file == NULL) {
    printf("Erro ao abrir o arquivo para escrita.\n");
    return -1;
}

fprintf(file, "digraph G {\n");
fprintf(file, "rankdir=TB; \n");

for (int i = 0; i < numaplicacoes; i++) {
    // Escapando caracteres especiais nas strings de label
    char escaped_label[MAX_LINE_LENGTH];
    escape_special_characters(aplicacoes[i].Label, escaped_label);

    fprintf(file, "  %d [label=\"%s\"];\n", aplicacoes[i].ID, escaped_label);
    for (int j = 0; j < aplicacoes[i].fd; j++) {
        char escaped_saida[MAX_LINE_LENGTH];
        escape_special_characters(aplicacoes[i].String_Saida, escaped_saida);
        fprintf(file, "  %d -> %d [label=\"Destino,%s\"];\n", aplicacoes[i].ID, aplicacoes[i].fornce_dados[j].ID, escaped_saida);
    }
    for (int j = 0; j < aplicacoes[i].fdb; j++) {
        char escaped_backup[MAX_LINE_LENGTH];
        escape_special_characters(aplicacoes[i].String_backup, escaped_backup);
        fprintf(file, "  %d -> %d [label=\"Backup,%s\"];\n", aplicacoes[i].ID, aplicacoes[i].fornece_dados_backp[j].ID, escaped_backup);
    }
}
fprintf(file, "}\n");
fclose(file);

    file = fopen("output/dados.txt", "w");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo de dados.\n");
        return -1;
    }
    for (int i = 0; i < numaplicacoes; i++) {
        int vazio = 1;
        fprintf(file, "Aplicacao %d\n", aplicacoes[i].ID);

        if(aplicacoes[i].ud > 0){
        vazio = 0;
        fprintf(file, "Usa dados de: ");
        for (int j = 0; j < aplicacoes[i].ud; j++) {
            fprintf(file, "%d", aplicacoes[i].usa_dados[j].ID);
             if (j < aplicacoes[i].ud - 1)  
              fprintf(file, ",");
        }
        fprintf(file, "\n");
        }
        if(aplicacoes[i].fd > 0){
        vazio = 0;
        fprintf(file, "Fornece dados pela saida para: ");
        for (int j = 0; j < aplicacoes[i].fd; j++) {
          
            fprintf(file, "%d", aplicacoes[i].fornce_dados[j].ID);
            if (j < aplicacoes[i].fd - 1)  
              fprintf(file, ",");

        }

        fprintf(file, "\n");
        }
        if(aplicacoes[i].fdb){
        vazio = 0;
        fprintf(file, "Fornece dados pelo backup para: ");
        for (int j = 0; j < aplicacoes[i].fdb; j++) {
            fprintf(file, "%d", aplicacoes[i].fornece_dados_backp[j].ID);
            if (j < aplicacoes[i].fdb - 1)  
              fprintf(file, ",");
        }
        fprintf(file, "\n");
        }
        if(vazio == 1){
          fprintf(file, "A aplicação não possui relações\n");
        }
         fprintf(file, "\n");
    }
    
    fprintf(file,"Alturas:\n");
    for(int i = 0; i < numaplicacoes; i++){
    
      if((aplicacoes[i].fd + aplicacoes[i].fdb) > 0 && aplicacoes[i].ud == 0){
         
          fprintf(file, "%d,1\n", aplicacoes[i].ID);

      }else if(aplicacoes[i].ud > 0 && (aplicacoes[i].fd + aplicacoes[i].fdb) > 0){
        fprintf(file, "%d,2\n", aplicacoes[i].ID);
      }else if(aplicacoes[i].ud > 0 && (aplicacoes[i].fd + aplicacoes[i].fdb) == 0){
        fprintf(file, "%d,3\n", aplicacoes[i].ID);
      }else{
        fprintf(file, "%d,4\n", aplicacoes[i].ID);
      }
    }

    fclose(file);
   
  for (int i = 0; i < numaplicacoes; i++) {
    //printf("Aplicacao %d\n", aplicacoes[i].ID);
    //printf("Usa dados de: ");
    for (int j = 0; j < aplicacoes[i].ud; j++) {
      //printf("%d,", aplicacoes[i].usa_dados[j].ID);
    }

    if(aplicacoes[i].ud > 0)free(aplicacoes[i].usa_dados);
    //printf("\n");
    //printf("Fornece dados pela saida para: ");
    for (int j = 0; j < aplicacoes[i].fd; j++) {
      //printf("%d,", aplicacoes[i].fornce_dados[j].ID);
    }
    //printf("\n");
    if(aplicacoes[i].ud > 0)free(aplicacoes[i].fornce_dados);
    //printf("Fornece dados pelo backup para: ");
    for (int j = 0; j < aplicacoes[i].fdb; j++) {
      //printf("%d,", aplicacoes[i].fornece_dados_backp[j].ID);
    }
    //printf("\n\n");
    if(aplicacoes[i].ud > 0)free(aplicacoes[i].fornece_dados_backp);
  }
  fclose(stream);
  free(aplicacoes);
  return 0;
}
