#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <time.h>
# include <sys/types.h>
# include <sys/stat.h>
# include <fcntl.h>
#include <sys/time.h>
#include <sys/resource.h>
#define BUTTON_PIN17 4
#define BUTTON_PIN18 5
FILE *output_file;
long int time_start,time_17,time_18,time_startn,time_18n,time_17n;
long double time1,time2,time3;//time stamps en segundos y en nano
char * myfifo = "/home/adam/myfifo";
int n,m;//Estos nos van a servir de mutex por los bounces
  struct timespec tp;

  clockid_t clk_id;
  char* Fmuestra="/run/user/1000/outF0";
  

void handler18(void){
	if(n==0){
		n=1;	
		clockid_t clk_id=CLOCK_MONOTONIC;
		struct timespec *xp;
        	xp=&tp;

                clock_gettime(clk_id,xp);
		time_18=xp->tv_sec;
         	time_18n=xp->tv_nsec;
		printf("m");//este priintf y las siguientes letras son para ver hasta donde llega el programa y como se ejecuta
                printf("%ld\n",time_18);
                printf("%ld\n",time_18n);
	   
 	
		piUnlock(1);//18 no dejaba, era un numero de 0 al 3
	}
}
void handler17(void){
	if(m==0){
		m=1;
        	clockid_t clk_id=CLOCK_MONOTONIC;
                struct timespec *xp;
        	xp=&tp;
                clock_gettime(clk_id,xp);
        	time_17=xp->tv_sec;
        	time_17n=xp->tv_nsec;
		printf("n");
		printf("%ld\n",time_17);
                printf("%ld\n",time_17n);
           

	}	
}

short exists(char *fname)
{
  int fd=open(fname, O_RDONLY);
  if (fd<0)         /* error */
    return 0;
  /* Si no hemos salido ya, cerramos */
  close(fd);
  return 1;
}



int main(int argc, char* argv[]){
	clk_id=CLOCK_MONOTONIC;// este es el que recomendaban para este tipo de funcionalidades hay 3 tipos mas
	m=0;
	n=0;
 if( clock_gettime(clk_id,&tp) == -1 ) {
      perror( "clock gettime" );
      exit( EXIT_FAILURE );
}


if ( (output_file = fopen(argv[2],"at")) == NULL ) {
        perror("Output file");
        exit(1);
        }//abre el fichero donde se van a guardar los timestamps

mkfifo(myfifo, 0666);//creamos la fifo y los permisos
char* message = argv[1]; //cogemos el mensaje que debe enviar tcpcli
char* muestra=argv[3];

    if (wiringPiSetup () < 0) {
      fprintf (stderr, "Unable to setup wiringPi: %s\n", strerror (errno));
return 1;
  }

   pinMode (BUTTON_PIN17, INPUT);
   pinMode (BUTTON_PIN18, INPUT);
   pullUpDnControl (BUTTON_PIN17, PUD_OFF);
   pullUpDnControl (BUTTON_PIN18, PUD_OFF);
   piLock(1);

if ( wiringPiISR (BUTTON_PIN17, INT_EDGE_RISING, &handler17) < 0 ) {
      fprintf (stderr, "Unable to setup ISR: %s\n", strerror (errno));
return 1;

}
printf("h");
if ( wiringPiISR (BUTTON_PIN18, INT_EDGE_RISING, &handler18) < 0 ) {
      fprintf (stderr, "Unable to setup ISR: %s\n", strerror (errno));
return 1;
  }

   

printf("i");
char result[44] ="./tcpcli "; 
    
strcat(result, message); 



printf("l");


while(exists(Fmuestra)==0){

		}
clock_gettime(clk_id,&tp);
time_start=tp.tv_sec;
time_startn=tp.tv_nsec;

nanosleep((const struct timespec[]){{0, 100000000L}}, NULL);
printf("w");
message[strlen(message)-1] = '\0';

printf("%s\n",muestra);
int r= system(result);
if(r!=0){
	system("sudo touch /run/user/1000/NO.txt");
}
piLock(1);
fprintf(output_file,"%s,%s ,%ld %ld,%ld %ld,%ld %ld\n",muestra,message,time_start,time_startn,time_17,time_17n,time_18,time_18n);
//Creo que me está sobreescribiendo el fichero todo el rato, pero bueno, es un fallo mínimo de momento.

fclose(output_file);
printf("x");
//nanosleep((const struct timespec[]){{0, 500000000L}}, NULL);

int fd;
fd = open(myfifo, O_WRONLY);
if (fd==-1) {
        perror("open error");
        exit(-1);
    }
printf("y");
write(fd, "Hi", sizeof("Hi"));
 
close(fd);
printf("z");

}





