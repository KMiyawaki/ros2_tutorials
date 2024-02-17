from setuptools import find_packages, setup

package_name = 'ros2_tutorials'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='K.Miyawaki',
    maintainer_email='5770105+KMiyawaki@users.noreply.github.com',
    description='ros2_tutorials',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_controller = ros2_tutorials.robot_controller:main'
        ],
    },
)
