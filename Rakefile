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

end
