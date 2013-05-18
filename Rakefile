require 'pathname'

# Find root directory
def repo_top_dir
  Pathname.new(File.dirname(__FILE__)).realpath
end

# Find current rpm name
def rpm_name
  name =Pathname(Rake.application.original_dir).relative_path_from(repo_top_dir).to_s.split('/').first
  # Make sure we're running from an rpm dir
  raise "Please run rake from an rpm directory!" if name == '.'
  return name
end

# Find top directory for the rpm
def top_dir
  Pathname.new("#{repo_top_dir}/#{rpm_name}").realpath
end

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
  build_script = "#{top_dir}/SPECS/#{rpm_name}.sh"
  if File.executable?(build_script)
    sh "cd #{top_dir}/SPECS; TOP_DIR=#{top_dir} bash #{rpm_name}.sh"
  else
    Rake::Task['rpm:build'].execute
  end
end

#---------------------------------------------------------------------------------------------------
namespace :rpm do
  build_flags = {
    :prepare => 'bp',
    :compile => 'bc',
    :install => 'bi',
    :build => 'ba'
  }

  def rpm_build(build_flag)
    "rpmbuild --define '_topdir #{top_dir}' -#{build_flag} #{rpm_name}.spec"
  end

  build_flags.each do |task_name, flag|
    desc "rpmbuild -#{flag}"
    task task_name.to_sym do
      sh "cd #{top_dir}/SPECS; #{rpm_build flag}"
    end
  end
end