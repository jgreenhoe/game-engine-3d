#include <stdio.h>
#include <stdbool.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL2_gfxPrimitives.h>

void draw_polygon(SDL_Window* screen, SDL_Renderer* renderer, int ROW,int COL,float polygon_float[][2][COL], float colors_float[][3]);
SDL_Window* create_SDL_window(const char* title, int x, int y, int width, int height, Uint32 flags);
SDL_Renderer* create_SDL_renderer(SDL_Window* screen, int index, Uint32 flags);
void clear_SDL_renderer(SDL_Renderer* renderer);
void present_SDL_renderer(SDL_Renderer* renderer);

int main(){
    float polygon[4][2][4] = {
    {{100, 450, 450, 100},
    {100, 100, 200, 200}},

    {{550, 900, 900, 550},
    {100, 100, 200, 200}},

    {{100, 450, 450, 100},
    {300, 300, 400, 400}},
    
    {{550, 900, 900, 550},
    {300, 300, 400, 400}}
    };
    float colors[4][3] = {
    {255, 255, 255},
    {255, 0, 0},
    {0, 255, 0},
    {0, 0, 255}
    };
    int ROW = sizeof(polygon)/sizeof(polygon[0]);
    int vertex_count = sizeof(polygon[0][0])/sizeof(polygon[0][0][0]);
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window* screen = create_SDL_window("Game Base", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 1915, 1000, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = create_SDL_renderer(screen, -1, 0);
    draw_polygon(screen, renderer, ROW, vertex_count, polygon, colors);
    present_SDL_renderer(renderer);
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
    
void clear_SDL_renderer(SDL_Renderer* renderer){
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0);
    SDL_RenderClear(renderer);
}
    
void present_SDL_renderer(SDL_Renderer* renderer){
    SDL_RenderPresent(renderer);
}

void draw_polygon(SDL_Window* screen, SDL_Renderer* renderer, int ROW, int COL, float polygon[][2][COL], float colors[][3]){
    int screen_width, screen_height;
    SDL_GetWindowSize(screen, &screen_width, &screen_height);
    
    Sint16 polygon_Sint[ROW][2][COL];
    for(int i = 0; i<ROW; i++){
        int num_vertex = sizeof(polygon[i][0])/sizeof(polygon[i][0][0]);
        int vertex_shown = num_vertex;
        for(int j = 0; j<num_vertex; j++){
            if (polygon[i][0][j] < 0 || polygon[i][0][j] > screen_width || polygon[i][1][j] < 0 || polygon[i][1][j] > screen_height){
                vertex_shown--;
            }
        }
        for(int j = 0; j<2; j++){
            for(int k = 0; k < COL; k++){
                polygon_Sint[i][j][k] = (Sint16) polygon[i][j][k];
            }
        }
        if(vertex_shown > 0){
            filledPolygonRGBA(renderer, polygon_Sint[i][0], polygon_Sint[i][1], COL, colors[i][0], colors[i][1], colors[i][2], 255);
        }
    }
}
