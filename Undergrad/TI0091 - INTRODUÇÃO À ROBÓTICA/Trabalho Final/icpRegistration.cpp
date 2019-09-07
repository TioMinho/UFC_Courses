/* ___________________ LIBRARIES ___________________ */
#include <algorithm>
#include <string>
#include <vector>
#include <iterator>
#include <iostream>
#include <boost/filesystem.hpp>
#include <pcl/io/pcd_io.h>      
#include <pcl/point_types.h>   
#include <pcl/registration/icp.h> 
#include <pcl/sample_consensus/ransac.h>
#include <pcl/sample_consensus/sac_model_plane.h>
#include <pcl/filters/statistical_outlier_removal.h>
#include <pcl/visualization/pcl_visualizer.h> 
#include <pcl/visualization/common/common.h> 

/* __________________ NAMESPACES ___________________ */
using namespace std;
using namespace pcl;

/* ______________ AUXILIARY FUNCTIONS ______________ */
struct path_leaf_string {
	std::string operator()(const boost::filesystem::directory_entry& entry) const {
		return entry.path().leaf().string();
	}
};

void read_directory(const std::string& name, vector<string>& v) {
	boost::filesystem::path p(name);
	boost::filesystem::directory_iterator start(p);
	boost::filesystem::directory_iterator end;
	std::transform(start, end, std::back_inserter(v), path_leaf_string());
}

bool compara(pcl::PointXYZ a, pcl::PointXYZ b) {
	if (a.x != b.x)return (a.x < b.x);
	return (a.z < b.z);
}

double dist(pcl::PointXYZ a, pcl::PointXYZ b) {
	return sqrt((a.x - b.x)*(a.x - b.x) + (a.y - b.y)*(a.y - b.y) + (a.z - b.z)*(a.z - b.z));
}

void filter_outliers(pcl::PointCloud< pcl::PointXYZ >::Ptr &cloud) {
	vector<int> aRemover;
	sort(cloud->points.begin(), cloud->points.end(), compara);
	double distLimite = 0.35, distMedia = 0, distAtual;

	int numPontos = cloud->points.size();
	int raioViz = 5, aux = 0;

	cout << "Num Pontos = " << numPontos << endl;

	int inicio;
	int densAtual, densLimite = 10, numRet = 0;
	for (int i = 0;i<numPontos;i++) {
		inicio = max(0, i - raioViz);
		densAtual = 0;
		for (int j = inicio; j < inicio + raioViz * 2; j++) {
			distAtual = dist(cloud->points[i], cloud->points[j]);
			distMedia += distAtual;
			aux++;
			if (distAtual < distLimite)
				densAtual++;
		}
		if (densAtual < densLimite) {
			aRemover.push_back(i);
			numRet++;
		}
	}

	while (!aRemover.empty()) {
		cloud->points.erase(cloud->points.begin() + aRemover.back());
		aRemover.pop_back();
	}

	cout << numRet << endl << (double) distMedia / aux << endl;
	cout << cloud->width << endl << cloud->height << endl;
	cloud->width = numPontos - numRet;
}

/* _________________ MAIN FUNCTION _________________ */
int main(int argc, char** argv)
{
	// VARIABLES
	vector < PointCloud<PointXYZ>::Ptr, Eigen::aligned_allocator <PointCloud <PointXYZ>::Ptr > > inputClouds;		// A vector of input clouds
	vector < PointCloud<PointXYZ>::Ptr, Eigen::aligned_allocator <PointCloud <PointXYZ>::Ptr > > outputClouds;		// A vector of output clouds
	pcl::PointCloud< pcl::PointXYZ >::Ptr cloud_final(new pcl::PointCloud< pcl::PointXYZ >);						// The resulting Cloud for the entire process
	pcl::PointCloud< pcl::PointXYZ >::Ptr cloud_filtered(new pcl::PointCloud< pcl::PointXYZ >);						// The resulting Cloud for the Outlier removal process
	pcl::PointCloud< pcl::PointXYZ >::Ptr cloud_ransac(new pcl::PointCloud< pcl::PointXYZ >);						// The resulting Cloud for the RANSAC process
	string dirName; vector<string> inputFiles; vector<string>::iterator it;
	float maxDist, tolerance;
	int maxIt;
	bool isFilter, isRansac;

	// WELCOME MESSAGE
	cout << "##########################################################################" << endl;
	cout << "#######################      ICP REGISTRATION      #######################" << endl;
	cout << "##########################################################################" << endl;

	// READING THE INPUT FILENAMES TROUGH THE USER
	
	cout << "## FILE INPUT ##" << endl;
	cout << "Enter the name of the directory containing the PCD files." << endl;
	cout << "Directory >> "; cin >> dirName; dirName = "data/" + dirName;

	read_directory(dirName, inputFiles);
	for (int i = 0; i < inputFiles.size(); i++) {
		if (inputFiles[i].substr(inputFiles[i].size() - 4, 4) != ".pcd") {
			inputFiles.erase(inputFiles.begin() + i); i--;
		}
	}

	cout << "\nINFO: Files founded:" << endl;
	for (int i = 0; i < inputFiles.size(); i++)
		cout << "( " << i+1 << " )" << " - " << inputFiles[i] << endl;

	int fileIdx, currentSize = inputFiles.size();
	cout << "\nEnter the index order, separated by spaces, of the ICP iterations." << endl;
	cout << ">> ";
	for (int i = 0; i < currentSize; i++) {
		cin >> fileIdx;
		if (fileIdx <= currentSize && fileIdx > 0) inputFiles.push_back(dirName + "/" + inputFiles[fileIdx - 1]);
		else cout << "ERROR: Value " << fileIdx << "out of bounds!" << endl;
	} 

	for (int i = 0; i < currentSize; i++) inputFiles.erase(inputFiles.begin());
	cout << endl;

	// LOADING THE POINT CLOUD DATA
	cout << "## LOADING DATA ##" << endl;

	for (it = inputFiles.begin(); it != inputFiles.end(); it++) {
		PointCloud<PointXYZ>::Ptr cloud_actual(new PointCloud<PointXYZ>);

		cout << "INFO: Loading file 'data/" << *it << "'" << endl;
		if (io::loadPCDFile<PointXYZ>(*it, *cloud_actual) != 0) {
			string errorMsg = "ERROR: Unable to find '" + *it + "'\n";
			PCL_ERROR(errorMsg.c_str());
			return -1;
		}

		inputClouds.push_back(cloud_actual);
	}
	cout << endl;

	///////////////////////////////////////////////////////////////////////////////////////////////////
	// ITERATIVE CLOSEST POINT
	cout << "## ICP OPTIMIZATION ##" << endl;
	cout << "Enter the values for the parameters:" << endl;
	cout << "Maximum Correspondence Distance >> "; cin >> maxDist;
	cout << "Maximum Number of Iterations >> "; cin >> maxIt;
	cout << "Minimum Tolerance Error >> "; cin >> tolerance;
	cout << "Apply Outlier Filtering? (1 - Yes, 0 - No) >> "; cin >> isFilter;
	cout << "Apply RANSAC? (1 - Yes, 0 - No) >> "; cin >> isRansac;


	pcl::IterativeClosestPoint<pcl::PointXYZ, pcl::PointXYZ> icp; 

	outputClouds.push_back(inputClouds[0]);
	for (int i = 1; i<inputClouds.size(); i++) {
		cout << "Info: Running ICP for " << inputFiles[i] << " -> " << inputFiles[i - 1] << endl;

		// TARGET AND SOURCE
		icp.setInputTarget(outputClouds.back());
		icp.setInputSource(inputClouds[i]);

		// HYPERPARAMETERS
		icp.setMaxCorrespondenceDistance(maxDist);
		icp.setMaximumIterations(maxIt);
		icp.setTransformationEpsilon(tolerance);

		// ICP
		pcl::PointCloud<pcl::PointXYZ>::Ptr result(new PointCloud<PointXYZ>);
		icp.align(*result);

		outputClouds.push_back(result);
		*cloud_final = (*cloud_final + *result);

		// ROTATION MATRIX VISUALIZATION
		Eigen::Matrix4f rotation_matrix;
		rotation_matrix = icp.getFinalTransformation();

		cout << "Convergence:" << icp.hasConverged() << " | Score: " << icp.getFitnessScore() << endl;
		cout << "Rotation Matrix:\n" << icp.getFinalTransformation() << endl;
		cout << endl;
	}

	cout << "Info: Optimization finished!" << endl;

	// SAVES THE RESULT
	// pcl::io::savePCDFileASCII("./data/Results/" + dirName + ".pcd", *cloud_final);
	// cout << "Info: Resulting PCD saved." << endl;
	
	///////////////////////////////////////////////////////////////////////////////////////////////////
	// FILTERING - CUSTOM FUNCTION
	// filter_outliers(cloud_final);
	// 
	
	///////////////////////////////////////////////////////////////////////////////////////////////////
	// FILTERING - USING PCL STATISTICALOUTLIERREMOVAL
	if (isFilter) {
		cout << "Info: Removing Outliers..." << endl;
		pcl::StatisticalOutlierRemoval<pcl::PointXYZ> sor;
		sor.setInputCloud(cloud_final);
		sor.setMeanK(50);
		sor.setStddevMulThresh(1.0);
		sor.filter(*cloud_final);
		cout << "Info: Outliers removed!" << endl;
	}

	///////////////////////////////////////////////////////////////////////////////////////////////////
	// RANSAC
	if (isRansac) {
		pcl::PointCloud< pcl::PointXYZ >::Ptr cloud_ransac_aux(new pcl::PointCloud< pcl::PointXYZ >);
		vector<vector<int> > planes(2, std::vector<int>(0));
		std::vector<int> inliers;

		// Back Wall
		for (int i = 0; i < cloud_final->points.size(); i++) {
			if (cloud_final->points[i].z > 2) planes[0].push_back(i);
			else planes[1].push_back(i);
		}

		pcl::copyPointCloud(*cloud_final, planes[0], *cloud_ransac_aux);

		pcl::SampleConsensusModelPlane<pcl::PointXYZ>::Ptr model_w1(new pcl::SampleConsensusModelPlane<pcl::PointXYZ>(cloud_ransac_aux));
		pcl::RandomSampleConsensus<pcl::PointXYZ> ransac(model_w1);
		ransac.setDistanceThreshold(.01);
		ransac.computeModel();
		ransac.getInliers(inliers);

		pcl::copyPointCloud(*cloud_ransac_aux, inliers, *cloud_ransac);
		pcl::copyPointCloud(*cloud_final, planes[1], *cloud_ransac_aux);
		(*cloud_ransac) = (*cloud_ransac + *cloud_ransac_aux);
		pcl::copyPointCloud(*cloud_ransac, *cloud_final);

		// Floor
		planes[0].clear(); planes[1].clear();
		for (int i = 0; i < cloud_final->points.size(); i++) {
			if (cloud_final->points[i].x > 0.3) planes[0].push_back(i);
			else planes[1].push_back(i);
		}

		pcl::copyPointCloud(*cloud_final, planes[0], *cloud_ransac_aux);

		pcl::SampleConsensusModelPlane<pcl::PointXYZ>::Ptr model_w2(new pcl::SampleConsensusModelPlane<pcl::PointXYZ>(cloud_ransac_aux));
		ransac.setSampleConsensusModel(model_w2);
		ransac.setDistanceThreshold(.01);
		ransac.computeModel();
		ransac.getInliers(inliers);

		pcl::copyPointCloud(*cloud_ransac_aux, inliers, *cloud_ransac);
		pcl::copyPointCloud(*cloud_final, planes[1], *cloud_ransac_aux);
		(*cloud_ransac) = (*cloud_ransac + *cloud_ransac_aux);
		pcl::copyPointCloud(*cloud_ransac, *cloud_final);
	}

	///////////////////////////////////////////////////////////////////////////////////////////////////

	// VISUALIZATION
	// 1º Viewer -> Registration
	boost::shared_ptr<pcl::visualization::PCLVisualizer> viewer(new pcl::visualization::PCLVisualizer("3D Viewer"));
	viewer->setBackgroundColor(0, 0, 0);

	for (int i = 0; i < outputClouds.size(); i++) {
		viewer->addPointCloud(outputClouds[i], "cloud_output_" + i);
		viewer->setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 2, "cloud_output_" + i);

		srand(94279*i);
		viewer->setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_COLOR, (rand() % 200) / 255.0, (rand() % 200) / 255.0, (rand() % 200) / 255.0, "cloud_output_" + i);
	}

	// 2º Viewer -> Registration after Outlier Removal
	boost::shared_ptr<pcl::visualization::PCLVisualizer> viewer2(new pcl::visualization::PCLVisualizer("3D Viewer"));
	viewer2->setBackgroundColor(0, 0, 0);

	viewer2->addPointCloud(cloud_final, "cloud_final");
	viewer2->setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 2, "cloud_final");
	viewer2->setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_COLOR, 0, 0, 1, "cloud_final");
	

	while (!viewer->wasStopped()) {
		viewer->spinOnce();
		viewer2->spinOnce();
		boost::this_thread::sleep(boost::posix_time::microseconds(100000));
	}
}
