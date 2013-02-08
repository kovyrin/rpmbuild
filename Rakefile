require 'pathname'

# Find root directory
repo_top_dir = Pathname.new(File.dirname(__FILE__)).realpath

# Find current rpm name
rpm_name = Pathname(Rake.application.original_dir).relative_path_from(repo_top_dir).to_s.split('/').first
raise "Please run rake from an rpm directory!" if rpm_name == '.'

# Find top directory for the rpm
top_dir = Pathname.new("#{repo_top_dir}/#{rpm_name}").realpath

#---------------------------------------------------------------------------------------------------
task :default => :build

desc "Clean build directory"
task :clean do
  sh "cd #{top_dir} && rm -rf BUILD SRPMS RPMS INSTALL BUILDROOT"
end

desc "Prepare build directory"
task :prepare do
  sh "cd #{top_dir} && mkdir BUILD SRPMS RPMS"
end

desc "Build RPM"
task :build => [ :clean, :prepare ] do
  sh "cd #{top_dir}/SPECS ; \
      if [[ -e #{rpm_name}.sh ]]; then
        TOP_DIR=#{top_dir} bash #{rpm_name}.sh
      else
        rpmbuild --define '_topdir #{top_dir}' -ba #{rpm_name}.spec
      fi
     "
end
