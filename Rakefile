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

  desc "contrast to noise difference"
  file "data/cnr.csv.gz" => ["contrast_to_noise.py", "data/cropped_reconstruction.h5"] do |f|
    sh "python #{f.source} #{f.prerequisites[1]} #{f.name}"
  end

end

namespace :video do
  
  desc "save video"
  file "data/video.mp4" => ["create_video.py", "data/filtered_reconstruction.h5"] do |f|
    sh "python #{f.source} #{f.prerequisites[1]} #{f.name}"
  end

end

namespace :plot do

  desc "plot position with R"
  file "data/position.png" => ["plot_position.R", "data/counts.csv"] do |f|
    sh "./#{f.source} -f #{f.prerequisites[1]} -o #{f.name}"
  end

  desc "plot contrast to noise difference"
  file "data/cnr.ratio.png" => ["contrast_to_noise.R", "data/cnr.csv.gz"] do |f|
    sh "./#{f.source} -f #{f.prerequisites[1]} -o #{f.name} -p data/cnr.absorption.png"
  end

  file "data/0.png" => ["plot_examples.py", "data/filtered_reconstruction.h5"] do |f|
    sh "python #{f.source} #{f.prerequisites[1]} #{f.name} -n 0"
  end

  file "data/100.png" => ["plot_examples.py", "data/filtered_reconstruction.h5"] do |f|
    sh "python #{f.source} #{f.prerequisites[1]} #{f.name} -n 100"
  end

  file "data/200.png" => ["plot_examples.py", "data/filtered_reconstruction.h5"] do |f|
    sh "python #{f.source} #{f.prerequisites[1]} #{f.name} -n 200"
  end

  desc "plot example images"
  task :examples => ["data/0.png", "data/100.png", "data/200.png"]
end
