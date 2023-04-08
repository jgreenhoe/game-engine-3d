#include <stdio.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>

void draw_polygon(SDL_Window* screen, SDL_Renderer* renderer, int ROW,int COL,int polygon[][2][COL]);
SDL_Window* create_SDL_window(const char* title, int x, int y, int width, int height, Uint32 flags);
SDL_Renderer* create_SDL_renderer(SDL_Window* screen, int index, Uint32 flags);

int main(){
//    Sint16 polygon[1][2][3] = {{{320, 380, 280},{240, 240, 300}}};
    int polygon[3][2][4] = {{{954.37901923, 957.5,957.5,954.36822415},
  {426.01194912, 425.99345399, 421.96290572, 422.03308702}},

 {{960.62098077, 957.5,957.5,960.61739893},
  {426.01194912,425.99345399, 430.76923077,430.72446812}},

 {{954.38260107, 957.5,957.5,954.37901923},
  {430.72446812, 430.76923077, 425.99345399, 426.01194912}}};
    int ROW = sizeof(polygon)/sizeof(polygon[0]);
    int vertex_count = sizeof(polygon[0][0])/sizeof(polygon[0][0][0]);
    SDL_Window* screen = create_SDL_window("Game Base", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 1915, 1000, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = renderer = SDL_CreateRenderer(screen, -1, 0);
    draw_polygon(screen, renderer, ROW, vertex_count, polygon);
}
SDL_Window* create_SDL_window(const char* title, int x, int y, int width, int height, Uint32 flags){
    SDL_Window* screen = SDL_CreateWindow(title, SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, width, height, SDL_WINDOW_SHOWN);
    return screen;
}
    
SDL_Renderer* create_SDL_renderer(SDL_Window* screen, int index, Uint32 flags){
    SDL_Renderer* renderer = SDL_CreateRenderer(screen, -1, 0);
    return renderer;
}

void draw_polygon(SDL_Window* screen, SDL_Renderer* renderer, int ROW,int COL,int polygon_int[][2][COL]){
    // Initialize SDL
    Sint16 polygon[ROW][2][COL];
    for (int i = 0; i < ROW; i++){
        for (int j = 0; j < 2; j++){
            for (int k = 0; k < COL; k++){
                polygon[i][j][k] = (Sint16) polygon_int[i][j][k];
            }
        }
    }
//    SDL_Window *screen;
//    SDL_Renderer *renderer;
//    if(SDL_WasInit(SDL_INIT_VIDEO)==0){
//        SDL_Init(SDL_INIT_VIDEO);
//        screen = SDL_CreateWindow("Game Base", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 1915, 1000, SDL_WINDOW_SHOWN);
//        renderer = SDL_CreateRenderer(screen, -1, 0);
//    }
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
    SDL_RenderClear(renderer);
    float r = 0;
    float g = 0;
    float b = 0;
    for(int i = 0; i<ROW; i++){
        filledPolygonRGBA(renderer, polygon[i][0], polygon[i][1], COL, r,g,b, 255);
        r += 0.3;
        g += 0.3;
        b += 0.3;
    }
    SDL_RenderPresent(renderer);
//    SDL_Delay(1000);
    
//    SDL_DestroyWindow(screen);
//    SDL_Quit();
}
