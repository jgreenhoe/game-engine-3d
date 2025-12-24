#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <SDL3/SDL.h>
#include <SDL3/SDL_render.h>
using namespace std;

int main(){
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window *window = SDL_CreateWindow("window", 1000, 1000, 0);
    SDL_Renderer *renderer = SDL_CreateRenderer(window, NULL);
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
    SDL_FColor colors[4] = {
    {1, 1, 1, 1},
    {1, 0, 0, 1},
    {0, 1, 0, 1},
    {0, 0, 1, 1}
    };
    SDL_Vertex shapes[4][4];
    for(int i=0; i < 4; i++){
        for(int k=0; k < 4; k++){
            shapes[i][k].position.x = polygon[i][0][k];
            shapes[i][k].position.y = polygon[i][1][k];
            shapes[i][k].color.r = 1.0;
            shapes[i][k].color.g = 0.0;
            shapes[i][k].color.b = 1.0;
            shapes[i][k].color.a = 1.0;
        }
    }
    bool quit = false;
    const int indices[3] = {0,1,2};
    while (!quit) {
        SDL_Event ev;
        while (SDL_PollEvent(&ev) != 0) {
            switch(ev.type) {
                case SDL_EVENT_QUIT:
                quit = true;
                break;
            }
        }
        SDL_SetRenderDrawColor(renderer, 50, 50, 50, 125);
        SDL_RenderClear(renderer);

        SDL_RenderGeometry(renderer, NULL, shapes[0], 4, indices, 3);

        SDL_RenderPresent(renderer);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}