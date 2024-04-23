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
//Baseparateste , Exemplo
int main() {

  char *arquivo = "Baseparateste.csv";
  char comando[200];

  // Primeiro %s chama a funcao e o segundo manda o 1o parametro
  sprintf(comando, "python ajustar.py %s", arquivo);
  system(comando);

  FILE *stream = fopen("func_data.csv", "r");
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

    char *temp = strtok(buffer, ",");
    aplicacoes[numaplicacoes].ID = atoi(temp);
    temp = strtok(NULL, ",");
    strcpy(aplicacoes[numaplicacoes].Label, temp);
    temp = strtok(NULL, ",");
    strcpy(aplicacoes[numaplicacoes].String_Entrada, temp);
    temp = strtok(NULL, ",");
    if (temp != NULL)
      strcpy(aplicacoes[numaplicacoes].String_Saida, temp);
    else
      strcpy(aplicacoes[numaplicacoes].String_Saida, "");
    temp = strtok(NULL, ",");
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
    printf("ID: %d, Label: %s, Entrada: %s, Saida: %s, Backup: %s\n",
           aplicacoes[numaplicacoes].ID, aplicacoes[numaplicacoes].Label,
           aplicacoes[numaplicacoes].String_Entrada,
           aplicacoes[numaplicacoes].String_Saida,
           aplicacoes[numaplicacoes].String_backup);

    numaplicacoes++;
    free(temp);
  }

  for (int i = 0; i < numaplicacoes; i++) {
    for (int j = 0; j < numaplicacoes; j++) {

      if (i != j) {
        if (strcmp(aplicacoes[i].String_Saida, aplicacoes[j].String_Entrada) ==
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
        if (strcmp(aplicacoes[i].String_backup, aplicacoes[j].String_Entrada) ==
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

  for (int i = 0; i < numaplicacoes; i++) {
    printf("Aplicacao %d\n", aplicacoes[i].ID);
    printf("Usa dados de: ");
    for (int j = 0; j < aplicacoes[i].ud; j++) {
      printf("%d,", aplicacoes[i].usa_dados[j].ID);
    }

    if(aplicacoes[i].ud > 0)free(aplicacoes[i].usa_dados);
    printf("\n");
    printf("Fornece dados pela saida para: ");
    for (int j = 0; j < aplicacoes[i].fd; j++) {
      printf("%d,", aplicacoes[i].fornce_dados[j].ID);
    }
    printf("\n");
    if(aplicacoes[i].ud > 0)free(aplicacoes[i].fornce_dados);
    printf("Fornece dados pelo backup para: ");
    for (int j = 0; j < aplicacoes[i].fdb; j++) {
      printf("%d,", aplicacoes[i].fornece_dados_backp[j].ID);
    }
    printf("\n\n");
    if(aplicacoes[i].ud > 0)free(aplicacoes[i].fornece_dados_backp);
  }
  fclose(stream);
  free(aplicacoes);
  return 0;
}
