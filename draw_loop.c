#include <stdio.h>
#include <stdbool.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>

void draw_polygon(SDL_Window* screen, SDL_Renderer* renderer, int ROW,int COL,int polygon[][2][COL]);
SDL_Window* create_SDL_window(const char* title, int x, int y, int width, int height, Uint32 flags);
SDL_Renderer* create_SDL_renderer(SDL_Window* screen, int index, Uint32 flags);

int main(){
    int polygon[4][2][4] = {
    {{100, 450, 450, 100},
    {100, 100, 200, 200}},

    {{550, 900, 900, 550},
    {100, 100, 200, 200}},

    {{100, 450, 450, 100},
    {300, 300, 400, 400}},
    
    {{550, 900, 900, 550},
    {300, 300, 400, 400}}
    };
    int ROW = sizeof(polygon)/sizeof(polygon[0]);
    int vertex_count = sizeof(polygon[0][0])/sizeof(polygon[0][0][0]);
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window* screen = create_SDL_window("Game Base", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 1915, 1000, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = create_SDL_renderer(screen, -1, 0);
    draw_polygon(screen, renderer, ROW, vertex_count, polygon);
    SDL_Delay(1000);
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
    int screen_width, screen_height;
    SDL_GetWindowSize(screen, &screen_width, &screen_height);
    Sint16 polygon[ROW][2][COL];
    for (int i = 0; i < ROW; i++){
        for (int j = 0; j < 2; j++){
            for (int k = 0; k < COL; k++){
                polygon[i][j][k] = (Sint16) polygon_int[i][j][k];
            }
        }
    }
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
    SDL_RenderClear(renderer);
    float r = 0;
    float g = 0;
    float b = 0;
    float increment = (float) 255/ROW;
    for(int i = 0; i<ROW; i++){
        int num_vertex = sizeof(polygon[i][0])/sizeof(polygon[i][0][0]);
        int vertex_shown = num_vertex;
        for(int j = 0; j<num_vertex; j++){
            if (polygon[i][0][j] < 0 || polygon[i][0][j] > screen_width || polygon[i][1][j] < 0 || polygon[i][1][j] > screen_height){
                vertex_shown--;
            }
        }
        if(vertex_shown > 0){
            filledPolygonRGBA(renderer, polygon[i][0], polygon[i][1], COL, r,g,b, 255);
            r += increment;
            g += increment;
            b += increment;
        }
    }
    SDL_RenderPresent(renderer);
//    SDL_Delay(1000);
    
//    SDL_DestroyWindow(screen);
//    SDL_Quit();
}
