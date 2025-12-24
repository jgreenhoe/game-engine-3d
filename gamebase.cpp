#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <SDL3/SDL.h>
//#include <SDL3/SDL_main.h>
using namespace std;

// convert obj file into class object
class Obj{
    public:
        struct vertex {float x, y, z;};
        vector<vertex> v;
        struct vtexture {float x, y;};
        vector<vtexture> vt;
        vector<vertex> vn;
        struct face {vector<int> fv, ft, fn;};
        vector<face> f;
        Obj(string filename){
            ifstream file(filename);
            string line;
            string prefix;
            while(getline(file, line)){
                //cout << line << endl;
                stringstream ss(line);
                ss >> prefix;
                if(prefix == "v"){
                    vertex vert;
                    ss >> vert.x >> vert.y >> vert.z;
                    v.push_back(vert);
                } else if(prefix == "vt"){
                    vtexture vtext;
                    ss >> vtext.x >> vtext.y;
                    vt.push_back(vtext);
                } else if(prefix == "vn"){
                    vertex vnorm;
                    ss >> vnorm.x >> vnorm.y >> vnorm.z;
                    vn.push_back(vnorm);
                } else if(prefix == "f"){
                    face fc;
                    string f_string;
                    //cout << stoi(f_string);
                    while(ss >> f_string){
                        int ind1 = f_string.find("/");
                        int ind2 = f_string.find("/", ind1+1);
                        fc.fv.push_back(stoi(f_string));
                        fc.ft.push_back(stoi(f_string.substr(ind1+1, ind2)));
                        fc.fn.push_back(stoi(f_string.substr(ind2+1, f_string.length())));
                    }
                }
            };
            file.close();
        };
        void setSize(double x, double y, double z){
            for(vertex i: v){
                i.x = i.x * x;
                i.y = i.y * y;
                i.z = i.z * z;
            }
        }
}; 

void render(Obj &obj);

int main() {
    if(!SDL_Init(SDL_INIT_VIDEO)){
        SDL_Log("SDL could not initialize! SDL error: %s\n", SDL_GetError());
        return 1;
    }
    static SDL_Window *window = SDL_CreateWindow("nigger", 800, 600, 0);
    static SDL_Renderer *renderer = NULL;
    string path_to_obj = "newell_teaset\\teapot.obj";
    Obj obj1(path_to_obj);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
};

void render(Obj &obj){
    
}