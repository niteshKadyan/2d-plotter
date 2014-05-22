#include <iostream>
#include <vector>
#include "cv.h"
#include "highgui.h"
#include <iostream>
#include <fstream>

using namespace cv;

class Node
{
    public:
	Node* parent;
	Node* child;
	int x, y;
	
	Node(int, int);
	Node();
};

Node::Node()
{
    this->x = -1;
    this->y = -1;
    parent = NULL;
    child = NULL;
}
Node::Node(int x, int y)
{
    this->x = x;
    this->y = y;
    parent = NULL;
    child = NULL;
}

std::vector<Node*> paths;

Node* generatePath(IplImage* img, int x, int y)
{
    int i, j, k, l, height, width, step, channels;
    
    height    = img->height;
    width     = img->width;
    step      = img->widthStep;
    channels  = img->nChannels;
    
    uchar *data = (uchar *)img->imageData; 
    
    if((x*step + y) < ((width-1) * (height-1)) && data[x*step + y] >= 100)
    {
	data[x*step + y] = 0;
	
	Node* start = new Node(x, y);
	std::cout << x << " " << y << "\n";
	int xnext = 0, ynext = 0;
	Node* next = new Node();
	
	if((x*step + y + 1) < ((width-1) * (height-1)) && (x*step + y + 1) > 0 && data[x*step + y + 1] >= 100)
	{
	    xnext = x;
	    ynext = y + 1;
	    std::cout << "1\n";
	    next = generatePath(img, xnext, ynext);
	}
	else if((x*step + y - 1) < ((width-1) * (height-1)) && (x*step + y - 1) > 0 && data[x*step + y - 1] >= 100)
	{
	    xnext = x;
	    ynext = y - 1;
	    std::cout << "2\n";
	    next = generatePath(img, xnext, ynext);
	}
	else if(((x + 1)*step + y) < ((width-1) * (height-1)) && ((x + 1)*step + y) > 0 && data[(x + 1)*step + y] >= 100)
	{
	    xnext = x + 1;
	    ynext = y;
	    std::cout << "3\n";
	    next = generatePath(img, xnext, ynext);
	}
	else if(((x + 1)*step + y + 1) < ((width-1) * (height-1)) && ((x + 1)*step + y + 1) > 0 && data[(x + 1)*step + y + 1] >= 100)
	{
	    xnext = x + 1;
	    ynext = y + 1;
	    std::cout << "4\n";
	    next = generatePath(img, xnext, ynext);
	}
	else if(((x + 1)*step + y - 1) < ((width-1) * (height-1)) && ((x + 1)*step + y - 1) > 0 && data[(x + 1)*step + y - 1] >= 100)
	{
	    xnext = x + 1;
	    ynext = y - 1;
	    std::cout << "5\n";
	    next = generatePath(img, xnext, ynext);
	}
	else if(((x - 1)*step + y) < ((width-1) * (height-1)) && ((x - 1)*step + y) > 0 && data[(x - 1)*step + y] >= 100)
	{
	    xnext = x - 1;
	    ynext = y;
	    std::cout << "6\n";
	    next = generatePath(img, xnext, ynext);
	}
	else if(((x - 1)*step + y + 1) < ((width-1) * (height-1)) && ((x - 1)*step + y + 1) > 0 && data[(x - 1)*step + y + 1] >= 100)
	{
	    xnext = x - 1;
	    ynext = y + 1;
	    std::cout << "7\n";
	    next = generatePath(img, xnext, ynext);
	}
	else if(((x - 1)*step + y - 1) < ((width-1) * (height-1)) &&  ((x - 1)*step + y - 1) > 0 && data[(x - 1)*step + y - 1] >= 100)
	{
	    xnext = x - 1;
	    ynext = y - 1;
	    std::cout << "8\n";
	    next = generatePath(img, xnext, ynext);
	}
	
	if(next->x != -1 && next->y != -1)
	    start->child = next;
	return start;
    }
    else
	return NULL;
}

void dumptoTxt()
{
    std::ofstream myfile("edges.txt");
    
    if (myfile.is_open())
    {
	vector<Node*>::const_iterator itr;
	for(itr = paths.begin(); itr != paths.end(); itr++)
	{
	    Node* node = *itr;
	    while(node != NULL)
	    {
		myfile << node->x << " " << node->y << "\n";
		node = node->child;
	    }
	    myfile << "1000 " << "1000\n";
	}
	myfile.close();
    }
}
int main(int argc, const char** argv )
{
    int edgeThresh = atoi(argv[1]);
    
    CvCapture *capture;
    capture = cvCaptureFromCAM(0);
    assert(capture);
    
    //cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, 320);
    //cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, 240);

    IplImage *image = cvQueryFrame(capture);
    //cvSaveImage("Maaaa.JPG", image);
    image = cvLoadImage("Maaaa.JPG");
    IplImage *gray = cvCreateImage(cvSize(image->width, image->height), IPL_DEPTH_8U, 1);
    IplImage *edges = cvCreateImage(cvSize(image->width, image->height), IPL_DEPTH_8U, 1);
    
    
    cvCvtColor(image, gray, CV_BGR2GRAY);
    cvCanny(gray, edges, edgeThresh, edgeThresh*3, 3);
    cvSaveImage("test.jpg", edges);
    
    image = cvLoadImage("test.jpg");
    cvCvtColor(image, gray, CV_BGR2GRAY);
    
    int height, width;
    height    = gray->height;
    width     = gray->width;

    //cvSaveImage("test.jpg", edges);
    
    for(int i = 0; i < height; i++)
	for(int j = 0; j < width; j++)
	{
	    Node *node = generatePath(gray, i, j);
	    //if(node != NULL)
		//std::cout << "\n";
	    int count = 0;
	    Node* start = node;
	    while(node != NULL)
	    {
		//std::cout << node->x << " " << node->y << " ";
		node = node->child;
		count++;
	    }
	    if(count >= 15 && start != NULL)
		paths.push_back(start);
	}
    //std::cout << "\n" << paths.size();
    dumptoTxt();
    return 0;
}
