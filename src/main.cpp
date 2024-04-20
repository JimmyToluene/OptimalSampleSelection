#include <glad/glad.h>
#include <GLFW/glfw3.h>

//#include <glm/glm.hpp>

#include <iostream>
#include <vector>

#include <cassert>
#include <filesystem>
#include <fstream>
#include <sstream>
#include <chrono>
#include <cmath>
#include <memory>
#include <algorithm>

//#define STB_IMAGE_WRITE_IMPLEMENTATION
//#include <stb_image_write.h>

#define ENABLE_LOG 1

#if ENABLE_LOG
#define LOG_INFO(...) printf(__VA_ARGS__)
#else
#define LOG_INFO(...)
#endif

#define MM_TIME_NOW() std::chrono::high_resolution_clock::now()
#define MM_TIMEPOINT decltype(MM_TIME_NOW())
#define MM_TIME_DELTA(x) (std::chrono::duration_cast<std::chrono::microseconds>(MM_TIME_NOW() - (x)).count() * 1e-6f)

int32_t LoadShader(const std::filesystem::path& path, uint32_t type)
{
	std::ifstream ifs(path);
	std::stringstream ss;
	ss << ifs.rdbuf();
	std::string str = ss.str();

	uint32_t id = glCreateShader(type);

	const char* cstr = str.c_str();
	glShaderSource(id, 1, &cstr, nullptr);
	glCompileShader(id);

	GLint isCompiled = 0;
	glGetShaderiv(id, GL_COMPILE_STATUS, &isCompiled);
	if (isCompiled == GL_FALSE)
	{
		GLint maxLength = 0;
		glGetShaderiv(id, GL_INFO_LOG_LENGTH, &maxLength);

		std::vector<GLchar> errorLog(maxLength);
		glGetShaderInfoLog(id, maxLength, &maxLength, &errorLog[0]);
		errorLog.push_back(0);

        std::cerr << errorLog.data() << std::endl;

		return -1;
	}

    return id;
}

void PrintTuple(int* tuple, uint32_t size)
{
    std::cout << "(";
    for (uint32_t i = 0; i < size; ++i) {
        std::cout << tuple[i];
        if (i != size - 1) 
            std::cout << ", ";
    }
    std::cout << ")\n";
}

// std430
struct KTuple
{
    int32_t tuple[8] = {0};
    int32_t score = 0;
};

// std430
struct JTuple
{
    int32_t tuple[8] = {0};
    //int32_t covered = 0;
};

template <typename T>
std::vector<T> Combinations(uint32_t n, uint32_t k)
{
    std::vector<T> result;

    std::string bitmask(k, 1); // K leading 1's
    bitmask.resize(n, 0); // N-K trailing 0's
 
    // print integers and permute bitmask
    do {
        result.emplace_back();
        for (uint32_t i = 0, j = 0; i < n; ++i) {
            if (bitmask[i]) {
                result.back().tuple[j++] = i+1;
            } 
        }
    } while (std::prev_permutation(bitmask.begin(), bitmask.end()));

    return result;
}

void GetCoverListFromImage(uint32_t image, uint32_t kIndex, std::vector<int32_t>& mem)
{
	glGetTextureSubImage(image, 0, 
		kIndex, 0, 0, 
		1, mem.size(), 1, 
		GL_RED_INTEGER, GL_INT, mem.size() * sizeof(int32_t), mem.data());
}

void GetCoverListFromImageArray(uint32_t image, uint32_t kIndex, uint32_t blockSizeX, uint32_t blockSizeY, uint32_t blockCountX, uint32_t blockCountY, std::vector<int32_t>& mem)
{
    // Get the index of the first block
    uint32_t z0 = kIndex / 4096;

    for (uint32_t z = z0, y = 0, remainedCount = mem.size(); y < blockCountY; z += blockCountX, ++y) {
        uint32_t offset = y * blockSizeY;
        uint32_t count = std::min(blockSizeY, remainedCount);
        //LOG_INFO("%s: z=%u, y=%u, offset=%u, count=%u, mem_size=%u\n", __FUNCTION__, z, y, offset, count, mem.size());
        glGetTextureSubImage(image, 0,
            kIndex % 4096, 0, z, 
            1, count, 1,
            GL_RED_INTEGER, GL_INT,
            count * sizeof(int32_t),
            &mem[offset]);
        remainedCount -= count;
    }
}

void 
MessageCallback( GLenum source,
                 GLenum type,
                 GLuint id,
                 GLenum severity,
                 GLsizei length,
                 const GLchar* message,
                 const void* userParam )
{
    if (type == GL_DEBUG_TYPE_ERROR) {
        std::cerr << message << std::endl;
    }
}

template <typename T>
void RemoveAt(T* arr, uint32_t len, uint32_t index) 
{
    for (uint32_t i = index; i < len - 1; ++i)
        arr[i] = arr[i + 1];
}

int main(void)
{
    static int32_t n = 20;
    static int32_t k = 7;
    static int32_t j = 5;
    static int32_t s = 3;

    /* Init tuples */ 

    auto kTuples = Combinations<KTuple>(n, k); 
    auto jTuples = Combinations<JTuple>(n, j); 

    uint32_t jTupleCount = jTuples.size();
    uint32_t remainedJTupleCount = jTupleCount;
    uint32_t remainedKTupleCount = kTuples.size();

    std::vector<KTuple> selectedKTuple;

    std::cout << "k-tuple count: " << remainedKTupleCount << std::endl;
    std::cout << "j-tuple count: " << jTupleCount << std::endl;

    /* Initialize the library */
    GLFWwindow* window;

    if (!glfwInit())
        return -1;

    /* Create a windowed mode window and its OpenGL context */
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6);
    window = glfwCreateWindow(640, 480, "Hello World", NULL, NULL);
    if (!window)
    {
        glfwTerminate();
        return -1;
    }

    /* Make the window's context current */
    glfwMakeContextCurrent(window);
    glfwSwapInterval(0);
    int version = gladLoadGL();
    if (version == 0) {
        printf("Failed to initialize OpenGL context\n");
        return -1;
    }

    /* Debug */
    glEnable(GL_DEBUG_OUTPUT);
    glDebugMessageCallback( MessageCallback, 0 );

    /***************************************** Quad shader *****************************************/
    int32_t quadVert = LoadShader("quad.vert", GL_VERTEX_SHADER);
    assert(quadVert >= 0);
    int32_t quadFrag = LoadShader("quad.frag", GL_FRAGMENT_SHADER);
    assert(quadVert >= 0);

    int32_t quadProgram = glCreateProgram();
    glAttachShader(quadProgram, quadVert);
    glAttachShader(quadProgram, quadFrag);
    glLinkProgram(quadProgram);
	GLint success = 0;
	glGetProgramiv(quadProgram, GL_LINK_STATUS, &success);
    if (success == GL_FALSE) {
        char info[512];
        glGetProgramInfoLog(quadProgram, sizeof(info), nullptr, info);
        std::cerr << info << std::endl;
        return -1;
    }

    uint32_t quadVAO;
    glCreateVertexArrays(1, &quadVAO);

    /***************************************** Compute shader ***************************************** /
    /* Load shader */
    int32_t compShader = LoadShader("example.comp", GL_COMPUTE_SHADER);
    assert(compShader >= 0);

    /* Link program */
    int32_t compProgram = glCreateProgram();
    glAttachShader(compProgram, compShader);
    glLinkProgram(compProgram);
	glGetProgramiv(compProgram, GL_LINK_STATUS, &success);
    if (success == GL_FALSE) {
        char info[512];
        glGetProgramInfoLog(compProgram, sizeof(info), nullptr, info);
        std::cerr << info << std::endl;
        return -1;
    }

    /* Uniforms */
    int32_t kTupleCountLoc = glGetUniformLocation(compProgram, "kTupleCount");
    //assert(kTupleCountLoc >= 0);
    int32_t jTupleCountLoc = glGetUniformLocation(compProgram, "jTupleCount");
    int32_t sLoc = glGetUniformLocation(compProgram, "s");
    int32_t jLoc = glGetUniformLocation(compProgram, "j");
    int32_t kLoc = glGetUniformLocation(compProgram, "k");
    int32_t blockCountXLoc = glGetUniformLocation(compProgram, "blockCountX");
    assert(jTupleCountLoc >= 0);
    assert(sLoc >= 0);
    assert(jLoc >= 0);
    assert(kLoc >= 0);

    /* K_tuples SSBO */
    uint32_t kTuplesSSBO;
    glCreateBuffers(1, &kTuplesSSBO);
    glNamedBufferData(kTuplesSSBO, kTuples.size() * sizeof(KTuple), kTuples.data(), GL_STATIC_DRAW);
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, kTuplesSSBO);

    /* J_tuples SSBO */
    uint32_t jTuplesSSBO;
    glCreateBuffers(1, &jTuplesSSBO);
    glNamedBufferData(jTuplesSSBO, jTuples.size() * sizeof(JTuple), jTuples.data(), GL_STATIC_DRAW);
    glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, jTuplesSSBO);

    /* Cover list image */
    //uint32_t coverListImage;
    //glCreateTextures(GL_TEXTURE_2D, 1, &coverListImage);
    //glTextureStorage2D(coverListImage, 1, GL_R8I, kTuples.size(), jTuples.size());
	//glBindImageTexture(0, coverListImage, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R8I);

    uint32_t coverListArray;
    uint32_t blockSizeX = 4096;
    uint32_t blockSizeY = 4096;
    uint32_t blockCountX = (uint32_t)std::ceilf((float)kTuples.size() / blockSizeX);
    uint32_t blockCountY = (uint32_t)std::ceilf((float)jTuples.size() / blockSizeY);
    uint32_t depth = blockCountX * blockCountY;
    std::cout << "Block count X: " << blockCountX << std::endl;
    std::cout << "Block count Y: " << blockCountY << std::endl;
    std::cout << "Depth: " << depth << std::endl;
    glCreateTextures(GL_TEXTURE_2D_ARRAY, 1, &coverListArray);
    glTextureStorage3D(coverListArray, 1, GL_R8I, blockSizeX, blockSizeY, depth);
    glBindImageTexture(1, coverListArray, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R8I);

	assert(glGetError() == 0);

	std::vector<int32_t> coverListMem(jTupleCount);

    /* Loop until the user closes the window */
    uint32_t iter = 0;
    auto start = MM_TIME_NOW();
    while (!glfwWindowShouldClose(window))
    {
        /* Render here */
        glClearColor(0.1, 0.1, 0.1, 1.0);
        glClear(GL_COLOR_BUFFER_BIT);

        /* Calculate score for each k-tuple on GPU */
        glUseProgram(compProgram);
        glUniform1i(jTupleCountLoc, remainedJTupleCount);
        glUniform1i(kTupleCountLoc, remainedKTupleCount);
        glUniform1i(sLoc, s);
        glUniform1i(jLoc, j);
        glUniform1i(kLoc, k);

        //std::cout << "\n-- iter " << iter++ << " --\n";
        LOG_INFO("\n-- iter %u --\n", iter++);

		/* Setup computation */
		static constexpr uint32_t localSizeX = 32;
		uint32_t workGroupCount = (uint32_t)std::ceilf((float)remainedKTupleCount / localSizeX);
        LOG_INFO("Workgroup count: %u\n", workGroupCount);

        glDispatchCompute(workGroupCount, 1, 1);
        glMemoryBarrier(GL_ALL_BARRIER_BITS);

        /* select the tuple with max coverage */
        int32_t bestKTupleIndex = 0;
        int32_t bestScore = 0;
        {
			KTuple* resultKTuples = (KTuple*)glMapNamedBuffer(kTuplesSSBO, GL_READ_WRITE);

			auto bestKTuple = std::max_element(resultKTuples, resultKTuples + remainedKTupleCount, 
				[](const KTuple& lhs, const KTuple& rhs) {
					return lhs.score < rhs.score; 
				});

            /* Move the best tuple to selected  */
            bestKTupleIndex = std::distance(resultKTuples, bestKTuple);
            bestScore = bestKTuple->score;

            selectedKTuple.push_back(*bestKTuple);
            RemoveAt(resultKTuples, remainedKTupleCount--, bestKTupleIndex);
            LOG_INFO("Remained k-tuple: %u\n", remainedKTupleCount);

			glUnmapNamedBuffer(kTuplesSSBO);
        }

        /* Actually cover with bestKTuple */
        {
            /* Get the cover list from image */
            //GetCoverListFromImage(coverListImage, bestKTupleIndex, coverListMem);
            GetCoverListFromImageArray(coverListArray, bestKTupleIndex, 4096, 4096, blockCountX, blockCountY, coverListMem);

            JTuple* resultJTuples = (JTuple*)glMapNamedBuffer(jTuplesSSBO, GL_READ_WRITE);
            for (uint32_t i = 0, indexOffset = 0; i < remainedJTupleCount; ++i) {
                if (coverListMem[i]) {
                    // Problem: remove invalidates the index
                    // Each remove shift the index after the point of remove by 1
                    // The score and number of tuples removed do not match
                    RemoveAt(resultJTuples, remainedJTupleCount, i - indexOffset++);
                }
            }
            remainedJTupleCount -= bestScore;

            LOG_INFO("Covered j-tuple: %u\n", bestScore);
            LOG_INFO("Remained j-tuple: %u\n", remainedJTupleCount);

            glUnmapNamedBuffer(jTuplesSSBO);
        }

        if (remainedJTupleCount == 0) {
            glfwSetWindowShouldClose(window, true);
        }

        /* Swap front and back buffers */
        glfwSwapBuffers(window);

        /* Poll for and process events */
        glfwPollEvents();
    }

    /* Print all selected groups */
	std::cout << " **** RESULT **** \n";
    for (uint32_t i = 0; i < selectedKTuple.size(); ++i) {
        std::cout << i << ": ";
        PrintTuple(selectedKTuple[i].tuple, k);
    }

    float elapsed = MM_TIME_DELTA(start);
    std::cout << "Elapsed time: " << elapsed << "s" << std::endl;

    glfwTerminate();
    return 0;
}