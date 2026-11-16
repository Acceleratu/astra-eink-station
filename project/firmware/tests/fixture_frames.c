/* Produce the exact deterministic SSD1683 controller data for the D02 bench procedure. */
#include "state.h"

#include <stdio.h>
#include <stdlib.h>

static int write_frame(const char *path, const uint8_t *raster, int pbm)
{
	FILE *out=fopen(path,"wb");
	if (!out) { return 1; }
	int failed=0;
	if (pbm) {
		if (fprintf(out,"P4\n%d %d\n",ASTRA_WIDTH,ASTRA_HEIGHT)<0) { failed=1; }
		for (size_t i=0; !failed && i<ASTRA_FRAME_BYTES; ++i) {
			failed=fputc((uint8_t)~raster[i],out)==EOF;
		}
	} else {
		failed=fwrite(raster,1,ASTRA_FRAME_BYTES,out)!=ASTRA_FRAME_BYTES;
	}
	return fclose(out)!=0 || failed;
}

int main(int argc,char **argv)
{
	if (argc!=2) { return 2; }
	int chamber=atoi(argv[1]);
	if (chamber!=15 && chamber!=25 && chamber!=35) { return 2; }
	int base=chamber==15?15:chamber-2;
	struct scene old={.seconds=45779,.pressure_pa=101325,.temp_centi_c=(int16_t)(base*100+68),
		.humidity_centi_pct=5000,.battery_mv=3900,.flags=ASTRA_UTC};
	struct scene next=old;
	next.seconds=132120;
	next.temp_centi_c=(int16_t)((base+1)*100+33);
	static uint8_t a[ASTRA_FRAME_BYTES], b[ASTRA_FRAME_BYTES];
	render_frame(&old,a); render_frame(&next,b);
	if (write_frame("old.raw",a,0) || write_frame("new.raw",b,0) ||
	    write_frame("old.pbm",a,1) || write_frame("new.pbm",b,1)) { return 1; }
	unsigned wb=0,bw=0,minx=ASTRA_WIDTH,miny=ASTRA_HEIGHT,maxx=0,maxy=0;
	for (unsigned y=0;y<ASTRA_HEIGHT;y++) {
		for (unsigned x=0;x<ASTRA_WIDTH;x++) {
			unsigned idx=y*ASTRA_WIDTH/8+x/8, mask=128u>>(x%8);
			if (!((a[idx]^b[idx]) & mask)) { continue; }
			if (a[idx]&mask) { ++wb; } else { ++bw; }
			if (x<minx) { minx=x; } if (x>maxx) { maxx=x; }
			if (y<miny) { miny=y; } if (y>maxy) { maxy=y; }
		}
	}
	printf("chamber=%d; old.temp_centi_c=%d; new.temp_centi_c=%d\n",chamber,old.temp_centi_c,next.temp_centi_c);
	printf("Changed rectangle (inclusive) [%u,%u]..[%u,%u]; white->black=%u, black->white=%u\n",
	       minx,miny,maxx,maxy,wb,bw);
	return !(wb>=100 && bw>=100 && miny==50 && maxy<86);
}
