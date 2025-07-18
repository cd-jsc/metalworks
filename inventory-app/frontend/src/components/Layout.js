import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  CubeIcon,
  BuildingStorefrontIcon,
  BuildingOfficeIcon,
  MapPinIcon,
  ChartBarIcon,
  ArrowsRightLeftIcon,
  BeakerIcon,
  TagIcon,
  TruckIcon,
  ClipboardDocumentListIcon,
  DocumentChartBarIcon,
  QrCodeIcon,
  PrinterIcon,
  Squares2X2Icon,
  SwatchIcon,
  Bars3Icon,
  XMarkIcon,
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { 
    name: 'Inventory', 
    children: [
      { name: 'Items', href: '/items', icon: CubeIcon },
      { name: 'Product Templates', href: '/product-templates', icon: Squares2X2Icon },
      { name: 'Product Variants', href: '/product-variants', icon: SwatchIcon },
      { name: 'Categories', href: '/categories', icon: TagIcon },
      { name: 'Tags', href: '/tags', icon: TagIcon },
      { name: 'Batches', href: '/batches', icon: BeakerIcon },
    ]
  },
  { 
    name: 'Locations', 
    children: [
      { name: 'Warehouses', href: '/warehouses', icon: BuildingOfficeIcon },
      { name: 'Locations', href: '/locations', icon: BuildingStorefrontIcon },
      { name: 'Bin Locations', href: '/bin-locations', icon: MapPinIcon },
    ]
  },
  { 
    name: 'Stock Management', 
    children: [
      { name: 'Stock Levels', href: '/stock-levels', icon: ChartBarIcon },
      { name: 'Stock Movements', href: '/stock-movements', icon: ArrowsRightLeftIcon },
      { name: 'Cycle Counts', href: '/cycle-counts', icon: ClipboardDocumentListIcon },
    ]
  },
  { 
    name: 'Operations', 
    children: [
      { name: 'Barcode Scanner', href: '/barcode-scanner', icon: QrCodeIcon },
      { name: 'Label Printing', href: '/label-printing', icon: PrinterIcon },
      { name: 'Suppliers', href: '/suppliers', icon: TruckIcon },
      { name: 'Reports', href: '/reports', icon: DocumentChartBarIcon },
    ]
  },
];

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

export default function Layout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [expandedSections, setExpandedSections] = useState({});
  const location = useLocation();

  const toggleSection = (sectionName) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionName]: !prev[sectionName]
    }));
  };

  const isCurrentPath = (href) => {
    return location.pathname === href;
  };

  const isSectionActive = (section) => {
    if (section.href) return isCurrentPath(section.href);
    if (section.children) {
      return section.children.some(child => isCurrentPath(child.href));
    }
    return false;
  };

  const renderNavItem = (item) => {
    if (item.children) {
      const isActive = isSectionActive(item);
      const isExpanded = expandedSections[item.name];
      
      return (
        <div key={item.name}>
          <button
            onClick={() => toggleSection(item.name)}
            className={classNames(
              'group flex items-center w-full px-2 py-2 text-sm font-medium rounded-md text-left',
              isActive ? 'bg-primary-100 text-primary-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            )}
          >
            <span className="flex-1">{item.name}</span>
            <svg
              className={classNames(
                'ml-2 h-4 w-4 transition-transform',
                isExpanded ? 'rotate-90' : 'rotate-0'
              )}
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
          {isExpanded && (
            <div className="ml-4 mt-1 space-y-1">
              {item.children.map((child) => (
                <Link
                  key={child.name}
                  to={child.href}
                  className={classNames(
                    isCurrentPath(child.href)
                      ? 'bg-primary-100 text-primary-900'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900',
                    'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
                  )}
                  onClick={() => setSidebarOpen(false)}
                >
                  <child.icon
                    className={classNames(
                      isCurrentPath(child.href)
                        ? 'text-primary-500'
                        : 'text-gray-400 group-hover:text-gray-500',
                      'mr-3 h-5 w-5'
                    )}
                  />
                  {child.name}
                </Link>
              ))}
            </div>
          )}
        </div>
      );
    }

    return (
      <Link
        key={item.name}
        to={item.href}
        className={classNames(
          isCurrentPath(item.href)
            ? 'bg-primary-100 text-primary-900'
            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900',
          'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
        )}
        onClick={() => setSidebarOpen(false)}
      >
        <item.icon
          className={classNames(
            isCurrentPath(item.href)
              ? 'text-primary-500'
              : 'text-gray-400 group-hover:text-gray-500',
            'mr-3 h-6 w-6'
          )}
        />
        {item.name}
      </Link>
    );
  };

  const getCurrentPageName = () => {
    for (const item of navigation) {
      if (item.href && isCurrentPath(item.href)) {
        return item.name;
      }
      if (item.children) {
        const activeChild = item.children.find(child => isCurrentPath(child.href));
        if (activeChild) {
          return activeChild.name;
        }
      }
    }
    return 'Dashboard';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar */}
      <div className={classNames(
        'fixed inset-0 z-40 lg:hidden',
        sidebarOpen ? 'block' : 'hidden'
      )}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        <div className="relative flex w-full max-w-xs flex-col bg-white">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              type="button"
              className="ml-1 flex h-10 w-10 items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              onClick={() => setSidebarOpen(false)}
            >
              <XMarkIcon className="h-6 w-6 text-white" />
            </button>
          </div>
          <div className="flex flex-shrink-0 items-center px-4 py-4">
            <h1 className="text-xl font-bold text-gray-900">Inventory System</h1>
          </div>
          <nav className="mt-5 flex-1 space-y-1 px-2 pb-4">
            {navigation.map(renderNavItem)}
          </nav>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex flex-col flex-grow bg-white border-r border-gray-200 pt-5 pb-4 overflow-y-auto">
          <div className="flex items-center flex-shrink-0 px-4">
            <h1 className="text-xl font-bold text-gray-900">Inventory System</h1>
          </div>
          <nav className="mt-5 flex-1 space-y-1 px-2 bg-white">
            {navigation.map(renderNavItem)}
          </nav>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top bar */}
        <div className="sticky top-0 z-10 bg-white shadow">
          <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
            <button
              type="button"
              className="border-r border-gray-200 px-4 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Bars3Icon className="h-6 w-6" />
            </button>
            <div className="flex items-center">
              <h2 className="text-lg font-medium text-gray-900">
                {getCurrentPageName()}
              </h2>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="h-8 w-8 rounded-full bg-primary-500 flex items-center justify-center">
                  <span className="text-sm font-medium text-white">A</span>
                </div>
                <span className="text-sm text-gray-700">Admin</span>
              </div>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}