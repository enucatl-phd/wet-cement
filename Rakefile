require "csv"

datasets = CSV.table "datasets.csv"

namespace :preprocessing do

  desc "crop all datasets and save reconstruction to data/ folder"
  file "data/cropped_reconstruction.h5" => ["crop_datasets.py"] + datasets[:reconstructed] do |f|
    sh "python #{f.prerequisites.join(" ")} --output #{f.name}"
  end

  desc "filter datasets"
  file "data/filtered_reconstruction.h5" => ["filter_reconstruction.py", "data/cropped_reconstruction.h5"] do |f|
    sh "python #{f.source} #{f.prerequisites[1]} #{f.name}"
  end

  desc "select region of interest"
  file "data/region_of_interest.h5" => ["region_selection.py", "data/filtered_reconstruction.h5"] do |f|
    sh "python #{f.source} #{f.prerequisites[1]} #{f.name}"
  end

end

namespace :analysis do

  desc "count wet pixels"
  file "data/counts.csv" => ["count_pixels.py", "data/region_of_interest.h5"] do |f|
    sh "python #{f.source} #{f.prerequisites[1]} #{f.name}"
  end

  desc "plot position with R"
  file "data/position.png" => ["plot_position.R", "data/counts.csv"] do |f|
    sh "./#{f.source} -f #{f.prerequisites[1]} -o #{f.name}"
  end

end

namespace :video do
  
  file "data/absorption.mp4" => ["create_video.py", "data/filtered_reconstruction.h5"] do |f|
    sh "python #{f.source} #{f.prerequisites[1]} #{f.name} 0"
  end

  file "data/ratio.mp4" => ["create_video.py", "data/filtered_reconstruction.h5"] do |f|
    sh "python #{f.source} #{f.prerequisites[1]} #{f.name} 2"
  end

  desc "save videos"
  task :all => ["data/absorption.mp4", "data/ratio.mp4"]

end
